from fastapi import APIRouter
from app.models.request import TryOnRequest
from app.services.renderer import *
from app.utils.image import decode_base64_image, encode_base64_image

router = APIRouter(prefix="/try-on", tags=["Try-On"])

@router.post("/render")
def render_tryon(req: TryOnRequest):
    canvas = decode_base64_image(req.imageBase64)

    if req.jewelry.get("earringId") and req.faceLandmarks:
        render_earrings(canvas, req.faceLandmarks, load_asset("app/assets/earrings/e.png"))

    if req.jewelry.get("necklaceId") and req.faceLandmarks:
        render_necklace(canvas, req.faceLandmarks, load_asset("app/assets/necklace/n.png"))

    if req.jewelry.get("ringId") and req.handLandmarks:
        render_ring(canvas, req.handLandmarks[0], load_asset("app/assets/ring/r.png"))

    if req.jewelry.get("braceletId") and req.handLandmarks:
        render_bracelet(canvas, req.handLandmarks[0], load_asset("app/assets/bracelet/b.png"))

    return {
        "resultImage": encode_base64_image(canvas)
    }
