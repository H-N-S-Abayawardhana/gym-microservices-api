from fastapi import APIRouter, HTTPException

from models import WorkoutPlan, WorkoutPlanCreate

router = APIRouter()

workout_plans: list[WorkoutPlan] = []
_next_plan_id = 1


@router.get("/")
def list_workout_plans():
    return {"items": workout_plans}


@router.get("/{plan_id}")
def get_workout_plan(plan_id: int):
    for plan in workout_plans:
        if plan.plan_id == plan_id:
            return plan
    raise HTTPException(status_code=404, detail="Workout plan not found")


@router.post("/")
def create_workout_plan(workout_plan: WorkoutPlanCreate):
    global _next_plan_id

    new_plan = WorkoutPlan(plan_id=_next_plan_id, **workout_plan.model_dump())
    _next_plan_id += 1
    workout_plans.append(new_plan)
    return new_plan


@router.put("/{plan_id}")
def update_workout_plan(plan_id: int, workout_plan_update: WorkoutPlanCreate):
    for i, plan in enumerate(workout_plans):
        if plan.plan_id == plan_id:
            updated_plan = WorkoutPlan(plan_id=plan_id, **workout_plan_update.model_dump())
            workout_plans[i] = updated_plan
            return updated_plan
    raise HTTPException(status_code=404, detail="Workout plan not found")


@router.delete("/{plan_id}")
def delete_workout_plan(plan_id: int):
    for i, plan in enumerate(workout_plans):
        if plan.plan_id == plan_id:
            del workout_plans[i]
            return {"message": "Workout plan deleted"}
    raise HTTPException(status_code=404, detail="Workout plan not found")
