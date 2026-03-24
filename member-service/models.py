from pydantic import BaseModel, Field


class MemberBase(BaseModel):
    email: str
    full_name: str = Field(..., min_length=1)


class MemberCreate(MemberBase):
    pass


class Member(MemberBase):
    id: str
