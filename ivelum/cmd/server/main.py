"""Точка входа FastAPI: приложение и роутер прокси Hacker News."""

import httpx
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.responses import Response

from configs.settings import settings
from internal.proxy.processor import process_html

app = FastAPI(title="Hacker News Proxy")
router = APIRouter()


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST"],
    responses={
        200: {"description": "Успешный ответ (HTML или контент с HN)"},
        502: {"description": "Ошибка при запросе к upstream (HN недоступен или ошибка)"},
    },
)
async def proxy(request: Request, path: str):
    """
    Проксирует запрос на Hacker News и возвращает модифицированный HTML или контент.

    - Модифицирует текст (™ после слов из 6 букв) и ссылки/формы для работы через прокси.
    - При ошибке запроса к upstream возвращает 502 Bad Gateway.
    """
    proxy_url = str(request.base_url).rstrip("/")
    target_url = f"{settings.hn_base_url}/{path}"

    params = dict(request.query_params)
    if params:
        target_url += "?" + "&".join(f"{k}={v}" for k, v in params.items())

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                target_url, follow_redirects=True, timeout=30.0
            )
            response.raise_for_status()

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
        except httpx.HTTPError:
            return HTMLResponse(
                content="Error fetching page from upstream",
                status_code=502,
            )


app.include_router(router)
