from fastapi import FastAPI

from routers.pieces import router as pieces_router

app = FastAPI()

app.include_router(pieces_router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
