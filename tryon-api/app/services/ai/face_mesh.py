import mediapipe as mp
import cv2

mp_face = mp.solutions.face_mesh.FaceMesh(static_image_mode=True)

def detect_face_landmarks(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = mp_face.process(rgb)

    if not result.multi_face_landmarks:
        return None

    return result.multi_face_landmarks[0].landmark
