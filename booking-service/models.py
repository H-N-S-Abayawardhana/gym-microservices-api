from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    member_id: int
    trainer_id: int
    session_date: str
    session_time: str
    booking_status: str = Field(default="Confirmed")


class BookingUpdate(BaseModel):
    member_id: int
    trainer_id: int
    session_date: str
    session_time: str
    booking_status: str


class Booking(BaseModel):
    booking_id: int
    member_id: int
    trainer_id: int
    session_date: str
    session_time: str
    booking_status: str
