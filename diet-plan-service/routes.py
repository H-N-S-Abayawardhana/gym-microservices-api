from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from db import get_conn

router = APIRouter()


class DietPlanCreate(BaseModel):
    member_id: int
    trainer_id: int
    goal: str = Field(..., min_length=1)
    meal_plan: str = Field(..., min_length=1)
    duration_weeks: int = Field(..., ge=0)


class DietPlan(DietPlanCreate):
    diet_plan_id: int


@router.get("/")
def list_diet_plans() -> dict:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT diet_plan_id, member_id, trainer_id, goal, meal_plan, duration_weeks
                FROM diet_plans
                ORDER BY diet_plan_id;
                """
            )
            rows = cur.fetchall()
    return {"items": [DietPlan(**row) for row in rows]}


@router.get("/{diet_plan_id}")
def get_diet_plan(diet_plan_id: int) -> dict:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT diet_plan_id, member_id, trainer_id, goal, meal_plan, duration_weeks
                FROM diet_plans
                WHERE diet_plan_id = %s;
                """,
                (diet_plan_id,),
            )
            row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Diet plan not found")
    return {"item": DietPlan(**row)}


@router.post("/")
def create_diet_plan(payload: DietPlanCreate) -> dict:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO diet_plans (
                    member_id, trainer_id, goal, meal_plan, duration_weeks
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING diet_plan_id, member_id, trainer_id, goal, meal_plan, duration_weeks;
                """,
                (
                    payload.member_id,
                    payload.trainer_id,
                    payload.goal,
                    payload.meal_plan,
                    payload.duration_weeks,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    return {"item": DietPlan(**row)}


@router.put("/{diet_plan_id}")
def update_diet_plan(diet_plan_id: int, payload: DietPlanCreate) -> dict:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE diet_plans
                SET member_id = %s,
                    trainer_id = %s,
                    goal = %s,
                    meal_plan = %s,
                    duration_weeks = %s
                WHERE diet_plan_id = %s
                RETURNING diet_plan_id, member_id, trainer_id, goal, meal_plan, duration_weeks;
                """,
                (
                    payload.member_id,
                    payload.trainer_id,
                    payload.goal,
                    payload.meal_plan,
                    payload.duration_weeks,
                    diet_plan_id,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    if not row:
        raise HTTPException(status_code=404, detail="Diet plan not found")
    return {"item": DietPlan(**row)}


@router.delete("/{diet_plan_id}")
def delete_diet_plan(diet_plan_id: int) -> dict:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM diet_plans WHERE diet_plan_id = %s RETURNING diet_plan_id;",
                (diet_plan_id,),
            )
            row = cur.fetchone()
        conn.commit()
    if not row:
        raise HTTPException(status_code=404, detail="Diet plan not found")
    return {"deleted": diet_plan_id}
