from pydantic import BaseModel


class AttendanceBase(BaseModel):
    member_id: str
    checked_in_at: str


class AttendanceCreate(AttendanceBase):
    pass


class Attendance(AttendanceBase):
    id: str
