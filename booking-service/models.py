from typing import Literal

from pydantic import BaseModel, Field

BookingStatus = Literal["Confirmed", "Cancelled"]


class BookingCreate(BaseModel):
    member_id: int
    trainer_id: int
    session_date: str
    session_time: str
    booking_status: BookingStatus = Field(default="Confirmed")


class BookingUpdate(BaseModel):
    member_id: int
    trainer_id: int
    session_date: str
    session_time: str
    booking_status: BookingStatus


class Booking(BaseModel):
    booking_id: int
    member_id: int
    trainer_id: int
    session_date: str
    session_time: str
    booking_status: BookingStatus
