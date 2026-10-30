from fastapi import FastAPI

from routers.pieces import router as pieces_router
from routers.clients import router as clients_router
from routers.auth import router as auth_router

app = FastAPI()

app.include_router(pieces_router, prefix="/api")
app.include_router(clients_router, prefix="/api")
app.include_router(auth_router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
