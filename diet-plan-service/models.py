from pydantic import BaseModel, Field


class DietPlanBase(BaseModel):
    name: str = Field(..., min_length=1)
    member_id: str
    daily_calories: int | None = None


class DietPlanCreate(DietPlanBase):
    pass


class DietPlan(DietPlanBase):
    id: str
