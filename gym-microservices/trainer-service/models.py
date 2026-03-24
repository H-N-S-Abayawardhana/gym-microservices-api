from pydantic import BaseModel, Field


class TrainerBase(BaseModel):
    email: str
    full_name: str = Field(..., min_length=1)
    specialties: list[str] = []


class TrainerCreate(TrainerBase):
    pass


class Trainer(TrainerBase):
    id: str
