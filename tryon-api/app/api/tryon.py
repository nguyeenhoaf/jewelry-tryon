from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
import cv2

from app.services.face_service import analyze_face
from app.services.pose_service import analyze_pose
from app.services.earring_service import apply_earring
from app.services.debug_landmarks import debug_landmarks_and_pose
from app.services.necklace_service import apply_necklace
from app.utils.image_utils import read_image_from_upload

router = APIRouter()

@router.post("/earring")
async def tryon_earring(
    user_image: UploadFile = File(...),
    earring_image: UploadFile = File(...)
):
    user_img = read_image_from_upload(user_image)
    earring_img = read_image_from_upload(earring_image, with_alpha=True)

    # Phân tích khuôn mặt và cơ thể
    face = analyze_face(user_img)
    
    # Kiểm tra xem có tìm thấy khuôn mặt (landmarks) không
    if face is None or face.landmarks is None:
        raise HTTPException(status_code=400, detail="No face detected in user image")

    # Thực hiện chèn khuyên tai
    output = apply_earring(user_img, earring_img, face) # Truyền cả object để service tự lấy landmarks

    _, png = cv2.imencode(".png", output)
    return Response(png.tobytes(), media_type="image/png")

@router.post("/necklace")
async def tryon_necklace(
    user_image: UploadFile = File(...),
    necklace_image: UploadFile = File(...)
):
    user_img = read_image_from_upload(user_image)
    necklace_img = read_image_from_upload(necklace_image, with_alpha=True)

    face = analyze_face(user_img)
    pose = analyze_pose(user_img)
    
    # Kiểm tra xem có đủ dữ liệu face và pose không
    # if analysis_result is None:
    #     raise HTTPException(status_code=400, detail="No user detected")
    
    # if analysis_result.landmarks is None:
    #     raise HTTPException(status_code=400, detail="Need both face and shoulders visible for necklace")

    # LỖI CŨ CỦA BẠN: Truyền nhầm earring_img vào đây
    # SỬA LẠI: Truyền necklace_img
    output = apply_necklace(
        user_img, 
        necklace_img, 
                face.landmarks,
        pose.pose_landmarks

    )

    _, png = cv2.imencode(".png", output)
    return Response(png.tobytes(), media_type="image/png")

@router.post("/debug-face")
async def debug_face(user_image: UploadFile = File(...)):
    user_img = read_image_from_upload(user_image)
    analysis_result = analyze_face(user_img)
    
    if not analysis_result or not analysis_result.landmarks:
        return {"error": "No face detected"}

    # Vẽ landmark lên ảnh
    debug_img = debug_landmarks_and_pose(user_img, analysis_result.landmarks)

    # Encode và trả về ảnh
    _, png = cv2.imencode(".png", debug_img)
    return Response(png.tobytes(), media_type="image/png")    