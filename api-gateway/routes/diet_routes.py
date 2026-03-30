from fastapi import APIRouter, Request

from .proxy_utils import proxy_request, service_url

router = APIRouter()

DIET_SERVICE_URL = service_url("DIET_SERVICE_URL", "http://127.0.0.1:8015")


@router.api_route("", methods=["GET", "POST"], include_in_schema=True)
async def diet_plans_collection(request: Request):
    return await proxy_request(request, DIET_SERVICE_URL, "/diet-plans")


@router.api_route("/{diet_plan_id}", methods=["GET", "PUT", "DELETE"], include_in_schema=True)
async def diet_plan_by_id(diet_plan_id: str, request: Request):
    return await proxy_request(request, DIET_SERVICE_URL, f"/diet-plans/{diet_plan_id}")
