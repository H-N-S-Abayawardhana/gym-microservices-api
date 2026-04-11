from pydantic import BaseModel


class TrainerBase(BaseModel):
    name: str
    specialty: str
    phone: str
    availability: str


class TrainerCreate(TrainerBase):
    pass


class Trainer(TrainerBase):
    trainer_id: int
