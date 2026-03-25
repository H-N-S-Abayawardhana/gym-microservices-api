from fastapi import FastAPI

from routes import router


app = FastAPI(title="Attendance Service", version="1.0.0")
app.include_router(router, prefix="/attendance", tags=["attendance"])


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8006, reload=True)
