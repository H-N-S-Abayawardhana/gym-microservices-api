from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_workout_plans():
    return {"items": []}
