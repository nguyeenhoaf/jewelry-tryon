import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands.Hands(static_image_mode=True)

def detect_hand_landmarks(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = mp_hands.process(rgb)

    if not result.multi_hand_landmarks:
        return None

    return result.multi_hand_landmarks[0].landmark
