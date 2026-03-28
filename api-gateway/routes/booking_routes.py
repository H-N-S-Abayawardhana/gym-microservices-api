import os

import httpx
from fastapi import APIRouter, Request, Response

BOOKING_SERVICE_URL = os.environ.get(
    "BOOKING_SERVICE_URL", "http://127.0.0.1:8011"
).rstrip("/")

router = APIRouter()


def _downstream_headers(request: Request) -> dict[str, str]:
    skip = {"host", "content-length", "connection"}
    return {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in skip
    }


async def _proxy(request: Request, downstream_path: str) -> Response:
    url = f"{BOOKING_SERVICE_URL}{downstream_path}"
    if request.url.query:
        url = f"{url}?{request.url.query}"
    body = await request.body()
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.request(
            request.method,
            url,
            content=body if body else None,
            headers=_downstream_headers(request),
        )
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type"),
    )


@router.api_route("", methods=["GET", "POST"], include_in_schema=True)
async def bookings_collection(request: Request):
    return await _proxy(request, "/bookings")


@router.api_route("/{booking_id}", methods=["GET", "PUT", "DELETE"], include_in_schema=True)
async def booking_by_id(booking_id: int, request: Request):
    return await _proxy(request, f"/bookings/{booking_id}")
