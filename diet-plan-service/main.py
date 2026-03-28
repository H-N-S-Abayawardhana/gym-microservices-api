from fastapi import FastAPI

from routes import router

app = FastAPI(title="Diet Plan Service")
app.include_router(router, prefix="/diet-plans", tags=["diet-plans"])

@app.get("/")
def root():
    return {"message": "Diet Plan Service Running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8015)
