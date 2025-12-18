import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True
)

class FaceResult:
    def __init__(self, landmarks):
        self.landmarks = landmarks  # normalized (x, y)

def analyze_face(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = mp_face_mesh.process(rgb)

    if not result.multi_face_landmarks:
        return None

    h, w = img.shape[:2]
    lm = result.multi_face_landmarks[0]

    # convert normalized → pixel
    landmarks = [
        (int(p.x * w), int(p.y * h))
        for p in lm.landmark
    ]

    return FaceResult(landmarks)
