from fastapi import FastAPI

from db import init_db
from routes import router

app = FastAPI(title="Attendance Service")
app.include_router(router, prefix="/attendance", tags=["attendance"])


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Attendance Service Running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8014)
