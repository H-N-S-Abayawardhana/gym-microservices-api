from fastapi import FastAPI

from db import init_db
from routes import router

app = FastAPI(title="Trainer Service")
app.include_router(router, prefix="/trainers", tags=["trainers"])


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Trainer Service Running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
