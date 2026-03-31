from fastapi import APIRouter, Request

from .proxy_utils import proxy_request, service_url
from .request_models import TrainerUpsertPayload

router = APIRouter()

TRAINER_SERVICE_URL = service_url("TRAINER_SERVICE_URL", "http://127.0.0.1:8012")


@router.get("", include_in_schema=True)
async def trainers_collection(request: Request):
    return await proxy_request(request, TRAINER_SERVICE_URL, "/trainers")


@router.post("", include_in_schema=True)
async def create_trainer(payload: TrainerUpsertPayload, request: Request):
    return await proxy_request(request, TRAINER_SERVICE_URL, "/trainers")


@router.get("/{trainer_id}", include_in_schema=True)
async def trainer_by_id(trainer_id: str, request: Request):
    return await proxy_request(request, TRAINER_SERVICE_URL, f"/trainers/{trainer_id}")


@router.put("/{trainer_id}", include_in_schema=True)
async def update_trainer(trainer_id: str, payload: TrainerUpsertPayload, request: Request):
    return await proxy_request(request, TRAINER_SERVICE_URL, f"/trainers/{trainer_id}")


@router.delete("/{trainer_id}", include_in_schema=True)
async def delete_trainer(trainer_id: str, request: Request):
    return await proxy_request(request, TRAINER_SERVICE_URL, f"/trainers/{trainer_id}")
