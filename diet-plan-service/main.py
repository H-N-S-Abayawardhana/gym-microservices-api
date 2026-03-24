from fastapi import FastAPI

from routes import router

app = FastAPI(title="Diet Plan Service")
app.include_router(router, prefix="/diet-plans", tags=["diet-plans"])


@app.get("/health")
def health():
    return {"status": "ok"}
