import cv2
import numpy as np

# Landmark chuẩn cho thùy tai (Earlobe)
LEFT_EAR_LOBE = 177  # Điểm bám tai trái
RIGHT_EAR_LOBE = 401 # Điểm bám tai phải
# Điểm dùng để đo độ rộng khuôn mặt (tính scale)
LEFT_CHEEK = 234 
RIGHT_CHEEK = 454

def apply_earring(user_img, earring_img, face):
    output = user_img.copy()
    lm = face.landmarks # Giả định lm là list các tuple (x, y) pixel

    # LEFT (Bên trái màn hình - Tai phải của người)
    output = place_earring(output, earring_img, lm, side="right")

    # RIGHT (Bên phải màn hình - Tai trái của người)
    # Lật khuyên tai để trông tự nhiên hơn
    flip_earring = cv2.flip(earring_img, 1)
    output = place_earring(output, flip_earring, lm, side="left")

    return output

def place_earring(bg, earring, lm, side):
    # Chọn điểm neo dựa trên phía
    if side == "left":
        anchor = lm[LEFT_EAR_LOBE]
        cheek = lm[LEFT_CHEEK]
    else:
        anchor = lm[RIGHT_EAR_LOBE]
        cheek = lm[RIGHT_CHEEK]

    # ===== 1. Tính toán tỷ lệ (Scaling) =====
    # Dựa trên khoảng cách giữa 2 má để biết mặt to hay nhỏ
    face_width = np.linalg.norm(np.array(lm[LEFT_CHEEK]) - np.array(lm[RIGHT_CHEEK]))
    
    # Giả định khuyên tai chiếm khoảng 15-20% chiều rộng khuôn mặt
    target_w = int(face_width * 0.18) 
    scale = target_w / earring.shape[1]
    target_h = int(earring.shape[0] * scale)

    earring_resized = cv2.resize(earring, (target_w, target_h))

    # ===== 2. Xác định vị trí (Positioning) =====
    # anchor[0], anchor[1] là tọa độ (x, y) của thùy tai
    # Chúng ta muốn đỉnh của khuyên tai bắt đầu từ thùy tai
    x = int(anchor[0] - target_w // 2)
    y = int(anchor[1] - int(target_h * 0.1))

    # Nếu khuyên tai quá sát má, có thể dịch chuyển nhẹ ra ngoài (offset)
    offset_x = int(face_width * 0.05) 
    if side == "left":
        x -= offset_x
    else:
        x += offset_x

    return overlay_rgba(bg, earring_resized, x, y)

def overlay_rgba(bg, fg, x, y):
    h, w = fg.shape[:2]
    bg_h, bg_w = bg.shape[:2]

    # Kiểm tra tràn viền
    if x < 0 or y < 0 or x + w > bg_w or y + h > bg_h:
        return bg

    # Tách kênh alpha
    alpha = fg[:, :, 3] / 255.0
    alpha_inv = 1.0 - alpha

    for c in range(0, 3):
        bg[y:y+h, x:x+w, c] = (alpha * fg[:, :, c] + alpha_inv * bg[y:y+h, x:x+w, c])

    return bg