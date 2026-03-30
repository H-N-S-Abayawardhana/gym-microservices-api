from pydantic import BaseModel, EmailStr
from typing import Optional


class Member(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    membership_type: str
    age: Optional[int] = None


class MemberCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    membership_type: str
    age: Optional[int] = None


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    membership_type: Optional[str] = None
    age: Optional[int] = None