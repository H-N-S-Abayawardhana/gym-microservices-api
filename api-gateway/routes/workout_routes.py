from fastapi import APIRouter, Request

from .proxy_utils import proxy_request, service_url

router = APIRouter()

WORKOUT_SERVICE_URL = service_url("WORKOUT_SERVICE_URL", "http://127.0.0.1:8013")


@router.api_route("", methods=["GET", "POST"], include_in_schema=True)
async def workout_plans_collection(request: Request):
    return await proxy_request(request, WORKOUT_SERVICE_URL, "/workout-plans")


@router.api_route("/{plan_id}", methods=["GET", "PUT", "DELETE"], include_in_schema=True)
async def workout_plan_by_id(plan_id: int, request: Request):
    return await proxy_request(request, WORKOUT_SERVICE_URL, f"/workout-plans/{plan_id}")
