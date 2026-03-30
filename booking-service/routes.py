from fastapi import APIRouter, HTTPException, status

from db import get_conn
from models import Booking, BookingCreate, BookingUpdate

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("", response_model=list[Booking])
def list_bookings():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT booking_id, member_id, trainer_id, session_date, session_time, booking_status
                FROM bookings
                ORDER BY booking_id;
                """
            )
            rows = cur.fetchall()
    return [Booking(**row) for row in rows]


@router.get("/{booking_id}", response_model=Booking)
def get_booking(booking_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT booking_id, member_id, trainer_id, session_date, session_time, booking_status
                FROM bookings
                WHERE booking_id = %s;
                """,
                (booking_id,),
            )
            row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found",
        )
    return Booking(**row)


@router.post("", response_model=Booking, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO bookings (member_id, trainer_id, session_date, session_time, booking_status)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING booking_id, member_id, trainer_id, session_date, session_time, booking_status;
                """,
                (
                    payload.member_id,
                    payload.trainer_id,
                    payload.session_date,
                    payload.session_time,
                    payload.booking_status,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    return Booking(**row)


@router.put("/{booking_id}", response_model=Booking)
def update_booking(booking_id: int, payload: BookingUpdate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE bookings
                SET member_id = %s,
                    trainer_id = %s,
                    session_date = %s,
                    session_time = %s,
                    booking_status = %s
                WHERE booking_id = %s
                RETURNING booking_id, member_id, trainer_id, session_date, session_time, booking_status;
                """,
                (
                    payload.member_id,
                    payload.trainer_id,
                    payload.session_date,
                    payload.session_time,
                    payload.booking_status,
                    booking_id,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found",
        )
    return Booking(**row)


@router.delete("/{booking_id}")
def delete_booking(booking_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM bookings WHERE booking_id = %s RETURNING booking_id;",
                (booking_id,),
            )
            row = cur.fetchone()
        conn.commit()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found",
        )
    return {"message": "Booking deleted successfully"}
