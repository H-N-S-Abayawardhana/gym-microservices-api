from fastapi import APIRouter, Request

from .proxy_utils import proxy_request, service_url
from .request_models import DietPlanUpsertPayload

router = APIRouter()

DIET_SERVICE_URL = service_url("DIET_SERVICE_URL", "http://127.0.0.1:8015")


@router.get("", include_in_schema=True)
async def diet_plans_collection(request: Request):
    return await proxy_request(request, DIET_SERVICE_URL, "/diet-plans")


@router.post("", include_in_schema=True)
async def create_diet_plan(payload: DietPlanUpsertPayload, request: Request):
    return await proxy_request(request, DIET_SERVICE_URL, "/diet-plans")


@router.get("/{diet_plan_id}", include_in_schema=True)
async def diet_plan_by_id(diet_plan_id: int, request: Request):
    return await proxy_request(request, DIET_SERVICE_URL, f"/diet-plans/{diet_plan_id}")


@router.put("/{diet_plan_id}", include_in_schema=True)
async def update_diet_plan(diet_plan_id: int, payload: DietPlanUpsertPayload, request: Request):
    return await proxy_request(request, DIET_SERVICE_URL, f"/diet-plans/{diet_plan_id}")


@router.delete("/{diet_plan_id}", include_in_schema=True)
async def delete_diet_plan(diet_plan_id: int, request: Request):
    return await proxy_request(request, DIET_SERVICE_URL, f"/diet-plans/{diet_plan_id}")
