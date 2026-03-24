from fastapi import FastAPI

from routes import router

app = FastAPI(title="Attendance Service")
app.include_router(router, prefix="/attendance", tags=["attendance"])


@app.get("/health")
def health():
    return {"status": "ok"}
