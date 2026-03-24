from fastapi import FastAPI

from routes import router

app = FastAPI(title="Member Service")
app.include_router(router, prefix="/members", tags=["members"])


@app.get("/health")
def health():
    return {"status": "ok"}
