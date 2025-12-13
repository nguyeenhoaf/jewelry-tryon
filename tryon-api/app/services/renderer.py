import numpy as np
from PIL import Image
from app.services.landmarks import FACE, HAND, lm
from app.services.geometry import midpoint, distance, angle_deg
from app.services.smoothing import EMA
from app.utils.image import decode_base64_image, encode_base64_image

ear_smoother = EMA()
ring_smoother = EMA()

def load_asset(path: str) -> Image.Image:
    return Image.open(path).convert("RGBA")

def paste(canvas, asset, center, scale, angle):
    w, h = asset.size
    asset = asset.resize((int(w * scale), int(h * scale)))
    asset = asset.rotate(angle, expand=True)
    x = int(center[0] - asset.size[0] / 2)
    y = int(center[1] - asset.size[1] / 2)
    canvas.alpha_composite(asset, (x, y))

def render_earrings(canvas, face_lms, asset):
    w, h = canvas.size
    for side in ["LEFT_EAR", "RIGHT_EAR"]:
        pts = [lm(face_lms[i], w, h) for i in FACE[side]]
        center = ear_smoother.apply(np.mean(pts, axis=0))
        paste(canvas, asset, center, 0.4, 0)

def render_necklace(canvas, face_lms, asset):
    w, h = canvas.size
    chin = lm(face_lms[FACE["CHIN"]], w, h)
    paste(canvas, asset, chin + np.array([0, 90]), 0.6, 0)

def render_ring(canvas, hand_lms, asset):
    w, h = canvas.size
    p1 = lm(hand_lms[HAND["RING_MCP"]], w, h)
    p2 = lm(hand_lms[HAND["RING_PIP"]], w, h)

    center = ring_smoother.apply(midpoint(p1, p2))
    angle = angle_deg(p1, p2)
    scale = distance(p1, p2) / 45

    paste(canvas, asset, center, scale, angle)

def render_bracelet(canvas, hand_lms, asset):
    w, h = canvas.size
    wrist = lm(hand_lms[HAND["WRIST"]], w, h)
    paste(canvas, asset, wrist, 0.5, 0)
