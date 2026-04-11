from pydantic import BaseModel, Field


class Attendance(BaseModel):
    """Row shape returned from the `attendance` table."""

    id: int = Field(..., description="Record identifier")
    member_id: int = Field(..., description="Member id")
    trainer_id: int = Field(..., description="Trainer id")
    session_type: str = Field(..., description="Session type, e.g. gym")
    date: str = Field(..., description="Session date (YYYY-MM-DD)")
    check_in_time: str = Field(..., description="Check-in time (HH:MM)")
    status: str = Field(..., description="Attendance status, e.g. present")


class AttendanceCreate(BaseModel):
    """Payload to create or update an attendance row."""

    member_id: int = Field(..., description="Member id")
    trainer_id: int = Field(..., description="Trainer id")
    session_type: str = Field(..., description="Session type, e.g. gym")
    date: str = Field(..., description="Session date (YYYY-MM-DD)")
    check_in_time: str = Field(..., description="Check-in time (HH:MM)")
    status: str = Field(..., description="Attendance status, e.g. present")


AttendanceResponse = Attendance
