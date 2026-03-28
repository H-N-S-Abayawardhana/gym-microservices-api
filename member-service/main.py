from fastapi import FastAPI

from routes import router

app = FastAPI(title="Member Service")
app.include_router(router, prefix="/members", tags=["members"])

@app.get("/")
def root():
    return {"message": "Booking Service Running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8016)
