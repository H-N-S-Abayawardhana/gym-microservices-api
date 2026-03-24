from pydantic import BaseModel


class BookingBase(BaseModel):
    member_id: str
    trainer_id: str
    starts_at: str


class BookingCreate(BookingBase):
    pass


class Booking(BookingBase):
    id: str
