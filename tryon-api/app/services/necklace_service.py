import cv2
import numpy as np
from app.utils.overlay_utils import overlay_rgba

# MediaPipe Pose & Face Mesh indexes
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
CHIN = 152

def apply_necklace(user_img, necklace_img, face_landmarks, pose_landmarks):
    output = user_img.copy()
    
    # 1. Lấy tọa độ
    l_sh = np.array(pose_landmarks[LEFT_SHOULDER])
    r_sh = np.array(pose_landmarks[RIGHT_SHOULDER])
    chin = np.array(face_landmarks[CHIN])
    
    # 2. Tính toán Scaling (Độ rộng)
    # Khoảng cách giữa 2 vai làm chuẩn để tính size vòng cổ
    shoulder_dist = np.linalg.norm(l_sh - r_sh)
    target_w = int(shoulder_dist * 0.55) # 0.5 - 0.6 thường là tỷ lệ đẹp cho vòng cổ
    
    scale = target_w / necklace_img.shape[1]
    target_h = int(necklace_img.shape[0] * scale)
    
    # Resize với chất lượng cao
    necklace_res = cv2.resize(necklace_img, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

    # 3. Xử lý xoay (Rotation) - Cực kỳ quan trọng nếu người đứng nghiêng
    # Tính góc nghiêng giữa 2 vai
    d_sh = l_sh - r_sh
    angle = np.degrees(np.arctan2(d_sh[1], d_sh[0]))
    # Chỉnh lại góc (vì vai trái thường cao hơn vai phải trong tọa độ ảnh)
    angle = angle if angle < 90 else angle - 180
    
    # Thực hiện xoay ảnh necklace
    M = cv2.getRotationMatrix2D((target_w // 2, target_h // 2), angle, 1.0)
    necklace_res = cv2.warpAffine(necklace_res, M, (target_w, target_h), 
                                  flags=cv2.INTER_LANCZOS4, 
                                  borderMode=cv2.BORDER_CONSTANT, 
                                  borderValue=(0,0,0,0))

    # 4. Xác định vị trí chèn (Positioning)
    # x: Lấy theo trục dọc của cằm để vòng luôn thẳng hàng với mặt
    x = int(chin[0] - target_w // 2)
    
    # y: Vòng cổ nên bắt đầu dưới cằm một khoảng dựa trên độ dài cổ
    # Khoảng cách cằm tới đường nối 2 vai
    neck_length = abs(((l_sh[1] + r_sh[1]) / 2) - chin[1])
    
    # Đặt y sao cho phần trên của vòng cổ cách cằm khoảng 20-30% chiều dài cổ
    y = int(chin[1] + neck_length * 0.25)

    # 5. Xử lý Alpha cho viền mượt (giống khuyên tai)
    b, g, r, a = cv2.split(necklace_res)
    a = cv2.GaussianBlur(a, (3, 3), 0)
    necklace_res = cv2.merge([b, g, r, a])

    return overlay_rgba(output, necklace_res, x, y)