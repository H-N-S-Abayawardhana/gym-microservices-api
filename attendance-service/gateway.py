from typing import Optional

import httpx
from fastapi import FastAPI, Response
from pydantic import BaseModel

ATTENDANCE_SERVICE = "http://localhost:8006"
ATTENDANCE_BASE = f"{ATTENDANCE_SERVICE}/attendance"

app = FastAPI(title="API Gateway", version="1.0.0")


class Attendance(BaseModel):
    member_id: int
    trainer_id: Optional[int] = None
    session_type: str
    date: str
    check_in_time: str
    status: str


def _build_response(upstream: httpx.Response) -> Response:
    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers={"content-type": upstream.headers.get("content-type", "application/json")},
    )


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/attendance")
async def forward_get_all():
    async with httpx.AsyncClient() as client:
        upstream = await client.get(f"{ATTENDANCE_BASE}/")
    return _build_response(upstream)


@app.get("/attendance/{attendance_id}")
async def forward_get_one(attendance_id: int):
    async with httpx.AsyncClient() as client:
        upstream = await client.get(f"{ATTENDANCE_SERVICE}/attendance/{attendance_id}")
    return _build_response(upstream)


@app.post("/attendance")
async def forward_create(attendance: Attendance):
    async with httpx.AsyncClient() as client:
        upstream = await client.post(
            f"{ATTENDANCE_BASE}/", json=attendance.model_dump()
        )
    return _build_response(upstream)


@app.put("/attendance/{attendance_id}")
async def forward_update(attendance_id: int, attendance: Attendance):
    async with httpx.AsyncClient() as client:
        upstream = await client.put(
            f"{ATTENDANCE_BASE}/{attendance_id}",
            json=attendance.model_dump(),
        )
    return _build_response(upstream)


@app.delete("/attendance/{attendance_id}")
async def forward_delete(attendance_id: int):
    async with httpx.AsyncClient() as client:
        upstream = await client.delete(f"{ATTENDANCE_BASE}/{attendance_id}")
    return _build_response(upstream)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("gateway:app", host="0.0.0.0", port=8000, reload=True)
