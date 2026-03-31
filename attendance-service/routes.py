from uuid import uuid4

from fastapi import APIRouter, HTTPException

from db import get_conn
from models import Attendance, AttendanceCreate, AttendanceResponse

router = APIRouter()


@router.get("/", response_model=list[AttendanceResponse])
def list_attendance():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, member_id, checked_in_at
                FROM attendance
                ORDER BY checked_in_at DESC;
                """
            )
            rows = cur.fetchall()
    return [Attendance(**row) for row in rows]


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance(attendance_id: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, member_id, checked_in_at
                FROM attendance
                WHERE id = %s;
                """,
                (attendance_id,),
            )
            row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return Attendance(**row)


@router.post("/", response_model=AttendanceResponse)
def create_attendance(payload: AttendanceCreate):
    attendance_id = str(uuid4())
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO attendance (id, member_id, checked_in_at)
                VALUES (%s, %s, %s)
                RETURNING id, member_id, checked_in_at;
                """,
                (attendance_id, payload.member_id, payload.checked_in_at),
            )
            row = cur.fetchone()
        conn.commit()
    return Attendance(**row)


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(attendance_id: str, payload: AttendanceCreate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE attendance
                SET member_id = %s, checked_in_at = %s
                WHERE id = %s
                RETURNING id, member_id, checked_in_at;
                """,
                (payload.member_id, payload.checked_in_at, attendance_id),
            )
            row = cur.fetchone()
        conn.commit()
    if not row:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return Attendance(**row)


@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM attendance WHERE id = %s RETURNING id;",
                (attendance_id,),
            )
            row = cur.fetchone()
        conn.commit()
    if not row:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return {"deleted": attendance_id}
