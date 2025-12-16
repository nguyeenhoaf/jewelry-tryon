import cv2
import numpy as np
from app.utils.overlay_utils import overlay_rgba

def apply_necklace(user_img, necklace_img, face):
    output = user_img.copy()
    lm = face.landmark_2d_106
    if lm is None:
        return output

    # ---- Landmarks ----
    chin = lm[57]
    jaw_left = lm[4]
    jaw_right = lm[12]

    # ---- Scale theo chiều rộng hàm ----
    jaw_width = np.linalg.norm(jaw_right - jaw_left)
    target_width = int(jaw_width * 1.3)   # hệ số có thể chỉnh

    scale = target_width / necklace_img.shape[1]
    new_h = int(necklace_img.shape[0] * scale)

    necklace_resized = cv2.resize(
        necklace_img,
        (target_width, new_h),
        interpolation=cv2.INTER_AREA
    )

    # ---- Position ----
    x = int(chin[0] - target_width // 2)
    y = int(chin[1] + jaw_width * 0.15)

    return overlay_rgba(output, necklace_resized, x, y)
