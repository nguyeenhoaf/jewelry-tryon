from fastapi import FastAPI
from app.api.tryon import router as tryon_router

app = FastAPI()

app.include_router(
    tryon_router,
    prefix="/tryon",
    tags=["Try-on"]
)
