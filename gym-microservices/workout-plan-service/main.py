from fastapi import FastAPI

from routes import router

app = FastAPI(title="Workout Plan Service")
app.include_router(router, prefix="/workout-plans", tags=["workout-plans"])


@app.get("/health")
def health():
    return {"status": "ok"}
