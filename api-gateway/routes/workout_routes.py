from fastapi import APIRouter, Request

from .proxy_utils import proxy_request, service_url
from .request_models import WorkoutPlanUpsertPayload

router = APIRouter()

WORKOUT_SERVICE_URL = service_url("WORKOUT_SERVICE_URL", "http://127.0.0.1:8013")


@router.get("", include_in_schema=True)
async def workout_plans_collection(request: Request):
    return await proxy_request(request, WORKOUT_SERVICE_URL, "/workout-plans/")


@router.post("", include_in_schema=True)
async def create_workout_plan(payload: WorkoutPlanUpsertPayload, request: Request):
    return await proxy_request(request, WORKOUT_SERVICE_URL, "/workout-plans/")


@router.get("/{plan_id}", include_in_schema=True)
async def workout_plan_by_id(plan_id: int, request: Request):
    return await proxy_request(request, WORKOUT_SERVICE_URL, f"/workout-plans/{plan_id}")


@router.put("/{plan_id}", include_in_schema=True)
async def update_workout_plan(plan_id: int, payload: WorkoutPlanUpsertPayload, request: Request):
    return await proxy_request(request, WORKOUT_SERVICE_URL, f"/workout-plans/{plan_id}")


@router.delete("/{plan_id}", include_in_schema=True)
async def delete_workout_plan(plan_id: int, request: Request):
    return await proxy_request(request, WORKOUT_SERVICE_URL, f"/workout-plans/{plan_id}")
