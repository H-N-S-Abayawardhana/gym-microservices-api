from fastapi import FastAPI

from routes import router

app = FastAPI(
    title="Booking Service",
    description="Gym session bookings (in-memory MVP).",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Booking Service Running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "booking"}
