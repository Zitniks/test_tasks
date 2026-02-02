"""Точка входа FastAPI: приложение и роутер прокси Hacker News."""

import logging
from contextlib import asynccontextmanager
from typing import Union
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, FastAPI, Request, status
from fastapi.responses import HTMLResponse, PlainTextResponse
from starlette.responses import Response

from configs.settings import settings
from internal.proxy.processor import process_html

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Общий HTTP-клиент для upstream (connection pooling), закрытие при остановке."""
    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=settings.request_timeout,
    ) as client:
        app.state.httpx_client = client
        yield
    app.state.httpx_client = None  # type: ignore[assignment]


app = FastAPI(title="Hacker News Proxy", lifespan=lifespan)
router = APIRouter()


def _build_target_url(path: str, query_params: dict) -> str:
    """Собирает URL upstream с корректно закодированными query-параметрами."""
    base_url = settings.hn_base_url.rstrip("/")
    base = f"{base_url}/{path.lstrip('/')}" if path else base_url
    if query_params:
        return f"{base}?{urlencode(query_params)}"
    return base


def _build_response(
    response: httpx.Response,
    proxy_url: str,
) -> Union[HTMLResponse, Response]:
    """Формирует ответ клиенту: HTML через process_html, остальное — как есть."""
    content_type = response.headers.get("content-type", "")
    if "text/html" in content_type:
        processed_html = process_html(response.text, proxy_url)
        return HTMLResponse(
            content=processed_html, status_code=response.status_code
        )
    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=content_type,
    )


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST"],
    responses={
        200: {"description": "Успешный ответ (HTML или контент с HN)"},
        502: {
            "description": (
                "502 Bad Gateway — ошибка при запросе к upstream (HN): "
                "таймаут, недоступность, HTTP-ошибка от HN."
            ),
        },
        503: {"description": "Сервис недоступен (клиент upstream не инициализирован)."},
        405: {"description": "Метод не разрешён (поддерживаются только GET и POST)."},
    },
)
async def proxy(
    request: Request, path: str
) -> Union[HTMLResponse, Response, PlainTextResponse]:
    """
    Проксирует запрос на Hacker News и возвращает модифицированный HTML или контент.

    - Поддерживаются методы GET и POST (тело POST передаётся в upstream).
    - Модифицирует текст (™ после слов из 6 букв) и ссылки/формы для работы через прокси.
    - При ошибке upstream возвращает 502 Bad Gateway.
    """
    http_client = getattr(request.app.state, "httpx_client", None)
    if http_client is None:
        logger.error("httpx_client not initialized")
        return PlainTextResponse(
            content="Service Unavailable",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    proxy_url = str(request.base_url).rstrip("/")
    query_params = dict(request.query_params)
    target_url = _build_target_url(path, query_params)

    try:
        if request.method == "GET":
            response = await http_client.get(target_url)
        elif request.method == "POST":
            body = await request.body()
            response = await http_client.post(target_url, content=body)
        else:
            return PlainTextResponse(
                content="Method Not Allowed",
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        response.raise_for_status()
        return _build_response(response, proxy_url)

    except httpx.HTTPError as e:
        logger.warning("Upstream error for %s: %s", target_url, e)
        return HTMLResponse(
            content="Error fetching page from upstream",
            status_code=502,
        )


app.include_router(router)
