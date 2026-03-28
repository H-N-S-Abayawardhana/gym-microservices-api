from fastapi import FastAPI

from routes import router

app = FastAPI(title="Workout Plan Service")
app.include_router(router, prefix="/workout-plans", tags=["workout-plans"])


@app.get("/")
def root():
    return {"message": "Workout Plan Service Running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8013)
