from fastapi import APIRouter, HTTPException
import uuid
from models import Trainer, TrainerCreate

router = APIRouter()

trainers = []


@router.get("/")
def list_trainers():
    return {"items": trainers}


@router.get("/{trainer_id}")
def get_trainer(trainer_id: str):
    for trainer in trainers:
        if trainer.trainer_id == trainer_id:
            return trainer
    raise HTTPException(status_code=404, detail="Trainer not found")


@router.post("/")
def create_trainer(trainer: TrainerCreate):
    trainer_id = str(uuid.uuid4())
    new_trainer = Trainer(trainer_id=trainer_id, **trainer.dict())
    trainers.append(new_trainer)
    return new_trainer


@router.put("/{trainer_id}")
def update_trainer(trainer_id: str, trainer_update: TrainerCreate):
    for i, trainer in enumerate(trainers):
        if trainer.trainer_id == trainer_id:
            updated_trainer = Trainer(trainer_id=trainer_id, **trainer_update.dict())
            trainers[i] = updated_trainer
            return updated_trainer
    raise HTTPException(status_code=404, detail="Trainer not found")


@router.delete("/{trainer_id}")
def delete_trainer(trainer_id: str):
    for i, trainer in enumerate(trainers):
        if trainer.trainer_id == trainer_id:
            del trainers[i]
            return {"message": "Trainer deleted"}
    raise HTTPException(status_code=404, detail="Trainer not found")
