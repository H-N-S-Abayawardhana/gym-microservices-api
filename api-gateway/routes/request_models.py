from typing import Literal

from pydantic import BaseModel, Field


class MemberCreatePayload(BaseModel):
    name: str
    email: str
    phone: str
    membership_type: str
    age: int | None = None


class MemberUpdatePayload(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    membership_type: str | None = None
    age: int | None = None


class TrainerUpsertPayload(BaseModel):
    name: str
    specialty: str
    phone: str
    availability: str


class WorkoutPlanUpsertPayload(BaseModel):
    member_id: int
    trainer_id: int
    goal: str
    duration_weeks: int
    difficulty_level: str
    notes: str | None = None


BookingStatus = Literal["Confirmed", "Cancelled"]


class BookingCreatePayload(BaseModel):
    member_id: int
    trainer_id: int
    session_date: str
    session_time: str
    booking_status: BookingStatus = Field(default="Confirmed")


class BookingUpdatePayload(BaseModel):
    member_id: int
    trainer_id: int
    session_date: str
    session_time: str
    booking_status: BookingStatus


class DietPlanUpsertPayload(BaseModel):
    member_id: int
    trainer_id: int
    goal: str = Field(..., min_length=1)
    meal_plan: str = Field(..., min_length=1)
    duration_weeks: int = Field(..., ge=0)


class AttendanceUpsertPayload(BaseModel):
    member_id: int
    trainer_id: int
    session_type: str
    date: str
    check_in_time: str
    status: str
