from fastapi import APIRouter, Request

from .proxy_utils import proxy_request, service_url
from .request_models import MemberCreatePayload, MemberUpdatePayload

router = APIRouter()

MEMBER_SERVICE_URL = service_url("MEMBER_SERVICE_URL", "http://127.0.0.1:8016")


@router.get("", include_in_schema=True)
async def members_collection(request: Request):
    return await proxy_request(request, MEMBER_SERVICE_URL, "/members")


@router.post("", include_in_schema=True)
async def create_member(payload: MemberCreatePayload, request: Request):
    return await proxy_request(request, MEMBER_SERVICE_URL, "/members")


@router.get("/{member_id}", include_in_schema=True)
async def member_by_id(member_id: int, request: Request):
    return await proxy_request(request, MEMBER_SERVICE_URL, f"/members/{member_id}")


@router.put("/{member_id}", include_in_schema=True)
async def update_member(member_id: int, payload: MemberUpdatePayload, request: Request):
    return await proxy_request(request, MEMBER_SERVICE_URL, f"/members/{member_id}")


@router.delete("/{member_id}", include_in_schema=True)
async def delete_member(member_id: int, request: Request):
    return await proxy_request(request, MEMBER_SERVICE_URL, f"/members/{member_id}")