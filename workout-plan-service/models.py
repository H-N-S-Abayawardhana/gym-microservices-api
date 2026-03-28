from typing import Optional

from pydantic import BaseModel


class WorkoutPlanBase(BaseModel):
    member_id: int
    trainer_id: int
    goal: str
    duration_weeks: int
    difficulty_level: str
    notes: Optional[str] = None


class WorkoutPlanCreate(WorkoutPlanBase):
    pass


class WorkoutPlan(WorkoutPlanBase):
    plan_id: int
