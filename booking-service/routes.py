from fastapi import APIRouter, HTTPException, status

from models import Booking, BookingCreate, BookingUpdate

router = APIRouter(prefix="/bookings", tags=["bookings"])

_bookings: list[Booking] = []
_next_booking_id: int = 1


def _find_index(booking_id: int) -> int:
    for i, b in enumerate(_bookings):
        if b.booking_id == booking_id:
            return i
    return -1


@router.get("", response_model=list[Booking])
def list_bookings():
    return _bookings


@router.get("/{booking_id}", response_model=Booking)
def get_booking(booking_id: int):
    idx = _find_index(booking_id)
    if idx == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found",
        )
    return _bookings[idx]


@router.post("", response_model=Booking, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate):
    global _next_booking_id
    booking = Booking(
        booking_id=_next_booking_id,
        member_id=payload.member_id,
        trainer_id=payload.trainer_id,
        session_date=payload.session_date,
        session_time=payload.session_time,
        booking_status=payload.booking_status,
    )
    _bookings.append(booking)
    _next_booking_id += 1
    return booking


@router.put("/{booking_id}", response_model=Booking)
def update_booking(booking_id: int, payload: BookingUpdate):
    idx = _find_index(booking_id)
    if idx == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found",
        )
    updated = Booking(
        booking_id=booking_id,
        member_id=payload.member_id,
        trainer_id=payload.trainer_id,
        session_date=payload.session_date,
        session_time=payload.session_time,
        booking_status=payload.booking_status,
    )
    _bookings[idx] = updated
    return updated


@router.delete("/{booking_id}")
def delete_booking(booking_id: int):
    idx = _find_index(booking_id)
    if idx == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found",
        )
    _bookings.pop(idx)
    return {"message": "Booking deleted successfully"}
