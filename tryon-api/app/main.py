from fastapi import FastAPI
from app.api.v1.tryon import router as tryon_router
from app.api.v1.jewelry import router as jewelry_router

app = FastAPI(
    title="Try-On Jewelry API",
    version="1.0.0"
)

app.include_router(tryon_router, prefix="/api/v1")
app.include_router(jewelry_router, prefix="/api/v1")
