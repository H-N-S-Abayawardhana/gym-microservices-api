from pydantic import BaseModel, Field


class WorkoutPlanBase(BaseModel):
    name: str = Field(..., min_length=1)
    member_id: str


class WorkoutPlanCreate(WorkoutPlanBase):
    pass


class WorkoutPlan(WorkoutPlanBase):
    id: str
