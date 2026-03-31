from fastapi import FastAPI

from routes.member_routes import router as member_router
from routes.trainer_routes import router as trainer_router
from routes.workout_routes import router as workout_router
from routes.booking_routes import router as booking_router
from routes.diet_routes import router as diet_router
from routes.attendance_routes import router as attendance_router

app = FastAPI(
    title="Gym API Gateway",
    description="Single HTTP entry point; routes forward to domain microservices.",
    version="1.0.0",
)

app.include_router(member_router, prefix="/members", tags=["members"])
app.include_router(trainer_router, prefix="/trainers", tags=["trainers"])
app.include_router(workout_router, prefix="/workout-plans", tags=["workout-plans"])
app.include_router(booking_router, prefix="/bookings", tags=["bookings"])
app.include_router(diet_router, prefix="/diet-plans", tags=["diet-plans"])
app.include_router(attendance_router, prefix="/attendance", tags=["attendance"])


@app.get("/")
def root():
    return {
        "message": "Gym API Gateway",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8010)
