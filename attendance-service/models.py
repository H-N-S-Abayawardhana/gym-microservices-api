from typing import Literal, Optional

from pydantic import BaseModel, Field


SessionType = Literal["gym", "personal_training", "class"]


class AttendanceBase(BaseModel):
    member_id: int = Field(..., description="Identifier of the member")
    trainer_id: Optional[int] = Field(None, description="Optional trainer identifier")
    session_type: SessionType = Field(..., description="Type of session attended")
    date: str = Field(..., description="Date of attendance (e.g., 2026-03-25)")
    check_in_time: str = Field(..., description="Check-in time (e.g., 09:00)")
    status: str = Field(..., description="Status of attendance record")


class AttendanceCreate(AttendanceBase):
    """Payload used to create attendance records."""


class AttendanceUpdate(AttendanceBase):
    """Payload used to update attendance records."""


class AttendanceResponse(AttendanceBase):
    attendance_id: int = Field(..., description="Auto-incremented attendance identifier")

    class Config:
        from_attributes = True
