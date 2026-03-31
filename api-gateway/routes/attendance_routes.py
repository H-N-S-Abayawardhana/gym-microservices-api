from fastapi import APIRouter, Request

from .proxy_utils import proxy_request, service_url

router = APIRouter()

ATTENDANCE_SERVICE_URL = service_url("ATTENDANCE_SERVICE_URL", "http://127.0.0.1:8014")


@router.api_route("", methods=["GET", "POST"], include_in_schema=True)
async def attendance_collection(request: Request):
    return await proxy_request(request, ATTENDANCE_SERVICE_URL, "/attendance")


@router.api_route("/{attendance_id}", methods=["GET", "PUT", "DELETE"], include_in_schema=True)
async def attendance_by_id(attendance_id: str, request: Request):
    return await proxy_request(request, ATTENDANCE_SERVICE_URL, f"/attendance/{attendance_id}")
