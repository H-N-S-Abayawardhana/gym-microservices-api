from fastapi import APIRouter, Request

from .proxy_utils import proxy_request, service_url
from .request_models import BookingCreatePayload, BookingUpdatePayload

BOOKING_SERVICE_URL = service_url("BOOKING_SERVICE_URL", "http://127.0.0.1:8011")

router = APIRouter()


@router.get("", include_in_schema=True)
async def bookings_collection(request: Request):
    return await proxy_request(request, BOOKING_SERVICE_URL, "/bookings")


@router.post("", include_in_schema=True)
async def create_booking(payload: BookingCreatePayload, request: Request):
    return await proxy_request(request, BOOKING_SERVICE_URL, "/bookings")


@router.get("/{booking_id}", include_in_schema=True)
async def booking_by_id(booking_id: int, request: Request):
    return await proxy_request(request, BOOKING_SERVICE_URL, f"/bookings/{booking_id}")


@router.put("/{booking_id}", include_in_schema=True)
async def update_booking(booking_id: int, payload: BookingUpdatePayload, request: Request):
    return await proxy_request(request, BOOKING_SERVICE_URL, f"/bookings/{booking_id}")


@router.delete("/{booking_id}", include_in_schema=True)
async def delete_booking(booking_id: int, request: Request):
    return await proxy_request(request, BOOKING_SERVICE_URL, f"/bookings/{booking_id}")
