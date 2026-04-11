from fastapi import APIRouter, HTTPException

from db import get_conn
from models import Attendance, AttendanceCreate, AttendanceResponse

router = APIRouter()

_SELECT = """
    SELECT id, member_id, trainer_id, session_type, "date", check_in_time, status
    FROM attendance
"""


@router.get("/", response_model=list[AttendanceResponse])
def list_attendance():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(f"{_SELECT} ORDER BY \"date\" DESC, check_in_time DESC;")
            rows = cur.fetchall()
    return [_row_to_attendance(row) for row in rows]


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance(attendance_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"{_SELECT} WHERE id = %s;",
                (attendance_id,),
            )
            row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return _row_to_attendance(row)


@router.post("/", response_model=AttendanceResponse)
def create_attendance(payload: AttendanceCreate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO attendance (
                    member_id, trainer_id, session_type, "date", check_in_time, status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, member_id, trainer_id, session_type, "date", check_in_time, status;
                """,
                (
                    payload.member_id,
                    payload.trainer_id,
                    payload.session_type,
                    payload.date,
                    payload.check_in_time,
                    payload.status,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    return _row_to_attendance(row)


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(attendance_id: int, payload: AttendanceCreate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE attendance
                SET member_id = %s,
                    trainer_id = %s,
                    session_type = %s,
                    "date" = %s,
                    check_in_time = %s,
                    status = %s
                WHERE id = %s
                RETURNING id, member_id, trainer_id, session_type, "date", check_in_time, status;
                """,
                (
                    payload.member_id,
                    payload.trainer_id,
                    payload.session_type,
                    payload.date,
                    payload.check_in_time,
                    payload.status,
                    attendance_id,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    if not row:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return _row_to_attendance(row)


@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: int):
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


def _row_to_attendance(row: dict) -> Attendance:
    d = row.get("date") or row.get("DATE")
    if d is not None and not isinstance(d, str) and hasattr(d, "isoformat"):
        d = d.isoformat()
    t = row["check_in_time"]
    if not isinstance(t, str) and hasattr(t, "strftime"):
        t = t.strftime("%H:%M")
    else:
        t = str(t)
        if len(t) >= 8 and t[2] == ":" and t[5] == ":":
            t = t[:5]
    return Attendance(
        id=int(row["id"]),
        member_id=int(row["member_id"]),
        trainer_id=int(row["trainer_id"]),
        session_type=str(row["session_type"]),
        date=str(d) if d is not None else "",
        check_in_time=t,
        status=str(row["status"]),
    )
