from fastapi import FastAPI
from db import init_db
from routes import router

app = FastAPI(title="Member Service")

app.include_router(router, prefix="/members", tags=["Members"])


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Member Service Running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8016)