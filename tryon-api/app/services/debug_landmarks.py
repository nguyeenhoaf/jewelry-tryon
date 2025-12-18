import cv2
import numpy as np
import math

def debug_landmarks(img, landmarks, color=(0, 255, 0)):
    """
    img: ảnh gốc (numpy array)
    landmarks: list các tọa độ [(x, y), ...]
    """
    debug_img = img.copy()
    for i, pt in enumerate(landmarks):
        # Vẽ vòng tròn tại điểm landmark
        cv2.circle(debug_img, pt, 2, color, -1)
        
        # Chỉ ghi số cho các điểm quan trọng để tránh bị rối mắt
        # Ví dụ: 150, 379 (tai), 152 (cằm), 234, 454 (má)
        important_pts = [150, 379, 152, 234, 454, 177, 401]
        if i in important_pts:
            cv2.putText(debug_img, str(i), (pt[0] + 2, pt[1] - 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            cv2.circle(debug_img, pt, 4, (0, 0, 255), -1) # Điểm quan trọng vẽ to hơn
            
    return debug_img

def debug_landmarks_and_pose(img, landmarks, color=(0, 255, 0)):
    """
    img: ảnh gốc (numpy array)
    landmarks: list [(x, y), ...] (MediaPipe pixel coords)
    """
    debug_img = img.copy()

    # ===== 1. Draw landmarks =====
    important_pts = [1, 33, 263, 152, 234, 454, 150, 379, 177, 401]

    for i, pt in enumerate(landmarks):
        cv2.circle(debug_img, pt, 2, color, -1)

        if i in important_pts:
            cv2.putText(
                debug_img,
                str(i),
                (pt[0] + 2, pt[1] - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 0, 255),
                1
            )
            cv2.circle(debug_img, pt, 4, (0, 0, 255), -1)

    # ===== 2. Head pose estimation (simple) =====
    nose = landmarks[1]
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    chin = landmarks[152]

    # Mid points
    eye_center = (
        int((left_eye[0] + right_eye[0]) / 2),
        int((left_eye[1] + right_eye[1]) / 2),
    )

    face_height = abs(chin[1] - eye_center[1])
    face_width = abs(right_eye[0] - left_eye[0])

    # ===== 3. Estimate angles =====
    # Yaw (left-right)
    yaw = (nose[0] - eye_center[0]) / max(face_width, 1)

    # Pitch (up-down)
    pitch = (nose[1] - eye_center[1]) / max(face_height, 1)

    # Roll (tilt)
    dy = right_eye[1] - left_eye[1]
    dx = right_eye[0] - left_eye[0]
    roll = math.atan2(dy, dx)

    # ===== 4. Draw pose axes =====
    axis_len = int(face_width * 0.5)

    origin = nose

    # X axis (yaw) – RED
    x_axis = (
        int(origin[0] + axis_len * yaw),
        origin[1]
    )

    # Y axis (pitch) – GREEN
    y_axis = (
        origin[0],
        int(origin[1] + axis_len * pitch)
    )

    # Z axis (roll) – BLUE (simulated)
    z_axis = (
        int(origin[0] + axis_len * math.cos(roll)),
        int(origin[1] + axis_len * math.sin(roll))
    )

    cv2.arrowedLine(debug_img, origin, x_axis, (0, 0, 255), 2)
    cv2.arrowedLine(debug_img, origin, y_axis, (0, 255, 0), 2)
    cv2.arrowedLine(debug_img, origin, z_axis, (255, 0, 0), 2)

    # ===== 5. Text overlay =====
    cv2.putText(
        debug_img,
        f"yaw={yaw:.2f} pitch={pitch:.2f} roll={math.degrees(roll):.1f}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    return debug_img