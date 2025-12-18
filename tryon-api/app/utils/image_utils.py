import cv2
import numpy as np

def read_image_from_upload(file, with_alpha=False):
    data = file.file.read()
    img = cv2.imdecode(
        np.frombuffer(data, np.uint8),
        cv2.IMREAD_UNCHANGED if with_alpha else cv2.IMREAD_COLOR
    )
    return img
