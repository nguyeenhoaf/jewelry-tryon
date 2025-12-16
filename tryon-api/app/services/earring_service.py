# app/services/earring_service.py
import cv2
import numpy as np
from app.utils.overlay_utils import overlay_rgba

def apply_earring(user_img, earring_img, face):
    output = user_img.copy()
    lm = face.landmark_2d_106
    if lm is None:
        return output

    # LEFT
    output = place_earring_stable(output, earring_img, lm, "left")

    # RIGHT
    flip = cv2.flip(earring_img, 1)
    output = place_earring_stable(output, flip, lm, "right")

    return output



def place_earring_stable(bg, earring, landmarks, side="left"):
    h, w = bg.shape[:2]

    # ---- Landmark indexes (InsightFace 106) ----
    if side == "left":
        eye = landmarks[33]     # left eye outer
        jaw = landmarks[4]      # left jaw
        direction = -1
    else:
        eye = landmarks[88]     # right eye outer
        jaw = landmarks[12]     # right jaw
        direction = 1

    # ---- Scale theo chiều cao mặt ----
    face_height = abs(jaw[1] - eye[1])
    target_height = int(face_height * 0.6)

    scale = target_height / earring.shape[0]
    new_w = int(earring.shape[1] * scale)

    earring_resized = cv2.resize(
        earring,
        (new_w, target_height),
        interpolation=cv2.INTER_AREA
    )

    # ---- Position ----
    x = int(eye[0] + direction * face_height * 0.15 - new_w // 2)
    y = int(eye[1] + face_height * 0.5)

    return overlay_rgba(bg, earring_resized, x, y)

