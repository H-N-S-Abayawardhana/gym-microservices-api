from fastapi import FastAPI

from routes import router

app = FastAPI(title="Booking Service")
app.include_router(router, prefix="/bookings", tags=["bookings"])


@app.get("/health")
def health():
    return {"status": "ok"}
