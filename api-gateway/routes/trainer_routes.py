from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_trainers():
    return {"items": []}
