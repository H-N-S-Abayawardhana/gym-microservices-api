from fastapi import APIRouter, HTTPException

from db import get_conn
from models import WorkoutPlan, WorkoutPlanCreate

router = APIRouter()


@router.get("/")
def list_workout_plans():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT plan_id, member_id, trainer_id, goal, duration_weeks, difficulty_level, notes
                FROM workout_plans
                ORDER BY plan_id;
                """
            )
            rows = cur.fetchall()
    return {"items": [WorkoutPlan(**row) for row in rows]}


@router.get("/{plan_id}")
def get_workout_plan(plan_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT plan_id, member_id, trainer_id, goal, duration_weeks, difficulty_level, notes
                FROM workout_plans
                WHERE plan_id = %s;
                """,
                (plan_id,),
            )
            row = cur.fetchone()
    if row:
        return WorkoutPlan(**row)
    raise HTTPException(status_code=404, detail="Workout plan not found")


@router.post("/")
def create_workout_plan(workout_plan: WorkoutPlanCreate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO workout_plans (
                    member_id, trainer_id, goal, duration_weeks, difficulty_level, notes
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING plan_id, member_id, trainer_id, goal, duration_weeks, difficulty_level, notes;
                """,
                (
                    workout_plan.member_id,
                    workout_plan.trainer_id,
                    workout_plan.goal,
                    workout_plan.duration_weeks,
                    workout_plan.difficulty_level,
                    workout_plan.notes,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    return WorkoutPlan(**row)


@router.put("/{plan_id}")
def update_workout_plan(plan_id: int, workout_plan_update: WorkoutPlanCreate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE workout_plans
                SET member_id = %s,
                    trainer_id = %s,
                    goal = %s,
                    duration_weeks = %s,
                    difficulty_level = %s,
                    notes = %s
                WHERE plan_id = %s
                RETURNING plan_id, member_id, trainer_id, goal, duration_weeks, difficulty_level, notes;
                """,
                (
                    workout_plan_update.member_id,
                    workout_plan_update.trainer_id,
                    workout_plan_update.goal,
                    workout_plan_update.duration_weeks,
                    workout_plan_update.difficulty_level,
                    workout_plan_update.notes,
                    plan_id,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    if row:
        return WorkoutPlan(**row)
    raise HTTPException(status_code=404, detail="Workout plan not found")


@router.delete("/{plan_id}")
def delete_workout_plan(plan_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM workout_plans WHERE plan_id = %s RETURNING plan_id;",
                (plan_id,),
            )
            row = cur.fetchone()
        conn.commit()
    if row:
        return {"message": "Workout plan deleted"}
    raise HTTPException(status_code=404, detail="Workout plan not found")
