from fastapi import FastAPI

from routes import router

app = FastAPI(title="Booking Service")

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Booking Service Running"}
