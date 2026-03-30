from typing import Dict
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class DietPlanCreate(BaseModel):
    member_id: str
    trainer_id: str
    goal: str = Field(..., min_length=1)
    meal_plan: str = Field(..., min_length=1)
    duration_weeks: int = Field(..., ge=0)


class DietPlan(DietPlanCreate):
    diet_plan_id: str


DIET_PLANS: Dict[str, DietPlan] = {}


def _get_or_404(diet_plan_id: str) -> DietPlan:
    plan = DIET_PLANS.get(diet_plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Diet plan not found")
    return plan


@router.get("/")
def list_diet_plans() -> dict:
    return {"items": list(DIET_PLANS.values())}


@router.get("/{diet_plan_id}")
def get_diet_plan(diet_plan_id: str) -> dict:
    return {"item": _get_or_404(diet_plan_id)}


@router.post("/")
def create_diet_plan(payload: DietPlanCreate) -> dict:
    diet_plan_id = str(uuid4())
    plan = DietPlan(diet_plan_id=diet_plan_id, **payload.model_dump())
    DIET_PLANS[diet_plan_id] = plan
    return {"item": plan}


@router.put("/{diet_plan_id}")
def update_diet_plan(diet_plan_id: str, payload: DietPlanCreate) -> dict:
    _get_or_404(diet_plan_id)  # validate existence
    updated = DietPlan(diet_plan_id=diet_plan_id, **payload.model_dump())
    DIET_PLANS[diet_plan_id] = updated
    return {"item": updated}


@router.delete("/{diet_plan_id}")
def delete_diet_plan(diet_plan_id: str) -> dict:
    _get_or_404(diet_plan_id)  # validate existence
    del DIET_PLANS[diet_plan_id]
    return {"deleted": diet_plan_id}
