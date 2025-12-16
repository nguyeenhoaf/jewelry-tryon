from fastapi import FastAPI
from app.api.tryon import router as tryon_router

app = FastAPI(title="AI Jewelry Try-On BE")

app.include_router(tryon_router, prefix="/tryon")

@app.get("/")
def health_check():
    return {"status": "ok"}
