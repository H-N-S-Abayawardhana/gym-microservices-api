from fastapi import APIRouter, HTTPException

from db import get_conn
from models import Trainer, TrainerCreate

router = APIRouter()


@router.get("/")
def list_trainers():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT trainer_id, name, specialty, phone, availability
                FROM trainers
                ORDER BY name;
                """
            )
            rows = cur.fetchall()
    return {"items": [Trainer(**row) for row in rows]}


@router.get("/{trainer_id}")
def get_trainer(trainer_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT trainer_id, name, specialty, phone, availability
                FROM trainers
                WHERE trainer_id = %s;
                """,
                (trainer_id,),
            )
            row = cur.fetchone()
    if row:
        return Trainer(**row)
    raise HTTPException(status_code=404, detail="Trainer not found")


@router.post("/")
def create_trainer(trainer: TrainerCreate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO trainers (name, specialty, phone, availability)
                VALUES (%s, %s, %s, %s)
                RETURNING trainer_id, name, specialty, phone, availability;
                """,
                (
                    trainer.name,
                    trainer.specialty,
                    trainer.phone,
                    trainer.availability,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    return Trainer(**row)


@router.put("/{trainer_id}")
def update_trainer(trainer_id: int, trainer_update: TrainerCreate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE trainers
                SET name = %s,
                    specialty = %s,
                    phone = %s,
                    availability = %s
                WHERE trainer_id = %s
                RETURNING trainer_id, name, specialty, phone, availability;
                """,
                (
                    trainer_update.name,
                    trainer_update.specialty,
                    trainer_update.phone,
                    trainer_update.availability,
                    trainer_id,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    if row:
        return Trainer(**row)
    raise HTTPException(status_code=404, detail="Trainer not found")


@router.delete("/{trainer_id}")
def delete_trainer(trainer_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM trainers WHERE trainer_id = %s RETURNING trainer_id;",
                (trainer_id,),
            )
            row = cur.fetchone()
        conn.commit()
    if row:
        return {"message": "Trainer deleted"}
    raise HTTPException(status_code=404, detail="Trainer not found")
