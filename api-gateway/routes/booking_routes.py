from fastapi import APIRouter, Request

from .proxy_utils import proxy_request, service_url

BOOKING_SERVICE_URL = service_url("BOOKING_SERVICE_URL", "http://127.0.0.1:8011")

router = APIRouter()


@router.api_route("", methods=["GET", "POST"], include_in_schema=True)
async def bookings_collection(request: Request):
    return await proxy_request(request, BOOKING_SERVICE_URL, "/bookings")


@router.api_route("/{booking_id}", methods=["GET", "PUT", "DELETE"], include_in_schema=True)
async def booking_by_id(booking_id: int, request: Request):
    return await proxy_request(request, BOOKING_SERVICE_URL, f"/bookings/{booking_id}")
