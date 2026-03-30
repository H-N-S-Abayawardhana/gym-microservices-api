import os

import httpx
from fastapi import Request, Response


def service_url(env_name: str, default: str) -> str:
    return os.environ.get(env_name, default).rstrip("/")


def downstream_headers(request: Request) -> dict[str, str]:
    skip = {"host", "content-length", "connection"}
    return {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in skip
    }


async def proxy_request(
    request: Request,
    upstream_base_url: str,
    downstream_path: str,
) -> Response:
    url = f"{upstream_base_url}{downstream_path}"
    if request.url.query:
        url = f"{url}?{request.url.query}"
    body = await request.body()
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.request(
            request.method,
            url,
            content=body if body else None,
            headers=downstream_headers(request),
        )
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type"),
    )
