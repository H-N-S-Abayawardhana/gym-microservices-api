from fastapi import APIRouter, Request

from .proxy_utils import proxy_request, service_url

router = APIRouter()

MEMBER_SERVICE_URL = service_url("MEMBER_SERVICE_URL", "http://127.0.0.1:8016")


@router.api_route("", methods=["GET", "POST"], include_in_schema=True)
async def members_collection(request: Request):
    return await proxy_request(request, MEMBER_SERVICE_URL, "/members")


@router.api_route("/{member_id}", methods=["GET", "PUT", "DELETE"], include_in_schema=True)
async def member_by_id(member_id: int, request: Request):
    return await proxy_request(request, MEMBER_SERVICE_URL, f"/members/{member_id}")