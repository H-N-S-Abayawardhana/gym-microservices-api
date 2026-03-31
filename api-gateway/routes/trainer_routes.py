from fastapi import APIRouter, Request

from .proxy_utils import proxy_request, service_url

router = APIRouter()

TRAINER_SERVICE_URL = service_url("TRAINER_SERVICE_URL", "http://127.0.0.1:8012")


@router.api_route("", methods=["GET", "POST"], include_in_schema=True)
async def trainers_collection(request: Request):
    return await proxy_request(request, TRAINER_SERVICE_URL, "/trainers")


@router.api_route("/{trainer_id}", methods=["GET", "PUT", "DELETE"], include_in_schema=True)
async def trainer_by_id(trainer_id: str, request: Request):
    return await proxy_request(request, TRAINER_SERVICE_URL, f"/trainers/{trainer_id}")
