from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

MEMBER_SERVICE_URL = "http://127.0.0.1:8016"


@router.get("/")
async def get_members():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MEMBER_SERVICE_URL}/members/")
        return response.json()


@router.get("/{member_id}")
async def get_member(member_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MEMBER_SERVICE_URL}/members/{member_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Member not found")
        return response.json()


@router.post("/")
async def create_member(member: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{MEMBER_SERVICE_URL}/members/", json=member)
        return response.json()


@router.put("/{member_id}")
async def update_member(member_id: int, member: dict):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{MEMBER_SERVICE_URL}/members/{member_id}", json=member)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Member not found")
        return response.json()


@router.delete("/{member_id}")
async def delete_member(member_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{MEMBER_SERVICE_URL}/members/{member_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Member not found")
        return response.json()