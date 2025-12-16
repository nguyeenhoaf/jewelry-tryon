# app/api/tryon.py
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response
import cv2

from app.services.face_service import analyze_face
from app.services.earring_service import apply_earring
from app.utils.image_utils import read_image_from_upload
from app.services.necklace_service import apply_necklace

router = APIRouter()

@router.post("/earring")
async def tryon_earring(
    user_image: UploadFile = File(...),
    earring_image: UploadFile = File(...)
):
    user_img = read_image_from_upload(user_image)
    earring_img = read_image_from_upload(earring_image, with_alpha=True)

    face = analyze_face(user_img)
    if face is None:
        return {"error": "No face detected"}

    output = apply_earring(user_img, earring_img, face)

    _, png = cv2.imencode(".png", output)
    return Response(content=png.tobytes(), media_type="image/png")

@router.post("/necklace")
async def tryon_necklace(
    user_image: UploadFile = File(...),
    necklace_image: UploadFile = File(...)
):
    user_img = read_image_from_upload(user_image)
    necklace_img = read_image_from_upload(necklace_image, with_alpha=True)

    face = analyze_face(user_img)
    if face is None:
        return {"error": "No face detected"}

    output = apply_necklace(user_img, necklace_img, face)

    _, png = cv2.imencode(".png", output)
    return Response(png.tobytes(), media_type="image/png")    
