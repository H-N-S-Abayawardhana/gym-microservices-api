from pydantic import BaseModel, Field


class Attendance(BaseModel):
    """Row shape returned from the `attendance` table."""

    id: str = Field(..., description="Record identifier")
    member_id: str = Field(..., description="Member identifier")
    checked_in_at: str = Field(..., description="Check-in timestamp")


class AttendanceCreate(BaseModel):
    """Payload to create or update an attendance row."""

    member_id: str = Field(..., description="Member identifier")
    checked_in_at: str = Field(..., description="Check-in timestamp")


# Name kept for existing route decorators / type hints
AttendanceResponse = Attendance
