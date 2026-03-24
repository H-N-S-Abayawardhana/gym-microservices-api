from fastapi import FastAPI

from routes import router

app = FastAPI(title="Trainer Service")
app.include_router(router, prefix="/trainers", tags=["trainers"])


@app.get("/health")
def health():
    return {"status": "ok"}
