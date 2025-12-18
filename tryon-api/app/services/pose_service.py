import cv2
import mediapipe as mp

# Khởi tạo Pose module
mp_pose = mp.solutions.pose.Pose(
    static_image_mode=True,
    model_complexity=1,
    enable_segmentation=False
)

class PoseResult:
    def __init__(self, landmarks):
        self.pose_landmarks = landmarks  # pixel coordinates (x, y)

def analyze_pose(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = mp_pose.process(rgb)

    if not result.pose_landmarks:
        return None

    h, w = img.shape[:2]
    
    # Convert normalized → pixel
    # Pose landmarks có 33 điểm chuẩn
    landmarks = [
        (int(p.x * w), int(p.y * h))
        for p in result.pose_landmarks.landmark
    ]

    return PoseResult(landmarks)