from fastapi import APIRouter, Request

from .proxy_utils import proxy_request, service_url
from .request_models import AttendanceUpsertPayload

router = APIRouter()

ATTENDANCE_SERVICE_URL = service_url("ATTENDANCE_SERVICE_URL", "http://127.0.0.1:8014")


@router.get("", include_in_schema=True)
async def attendance_collection(request: Request):
    return await proxy_request(request, ATTENDANCE_SERVICE_URL, "/attendance")


@router.post("", include_in_schema=True)
async def create_attendance(payload: AttendanceUpsertPayload, request: Request):
    return await proxy_request(request, ATTENDANCE_SERVICE_URL, "/attendance")


@router.get("/{attendance_id}", include_in_schema=True)
async def attendance_by_id(attendance_id: int, request: Request):
    return await proxy_request(request, ATTENDANCE_SERVICE_URL, f"/attendance/{attendance_id}")


@router.put("/{attendance_id}", include_in_schema=True)
async def update_attendance(attendance_id: int, payload: AttendanceUpsertPayload, request: Request):
    return await proxy_request(request, ATTENDANCE_SERVICE_URL, f"/attendance/{attendance_id}")


@router.delete("/{attendance_id}", include_in_schema=True)
async def delete_attendance(attendance_id: int, request: Request):
    return await proxy_request(request, ATTENDANCE_SERVICE_URL, f"/attendance/{attendance_id}")
