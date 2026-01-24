from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.responses import Response

import httpx

from configs.settings import settings
from internal.proxy.processor import process_html

app = FastAPI(title='Hacker News Proxy')


@app.api_route('/{path:path}', methods=['GET', 'POST'])
async def proxy(request: Request, path: str):
    proxy_url = request.base_url._url.rstrip('/')
    target_url = f'{settings.hn_base_url}/{path}'

    params = dict(request.query_params)
    if params:
        target_url += '?' + '&'.join(f'{k}={v}' for k, v in params.items())

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url, follow_redirects=True, timeout=30.0)
            response.raise_for_status()

            if 'text/html' in response.headers.get('content-type', ''):
                processed_html = process_html(response.text, proxy_url)
                return HTMLResponse(content=processed_html, status_code=response.status_code)
            else:
                return Response(
                    content=response.content,
                    status_code=response.status_code,
                    media_type=response.headers.get('content-type'),
                )
        except httpx.HTTPError:
            return HTMLResponse(content='Error fetching page', status_code=500)
