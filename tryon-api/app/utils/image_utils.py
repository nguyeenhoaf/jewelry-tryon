import numpy as np
import cv2

def read_image_from_upload(upload_file, with_alpha=False):
    content = upload_file.file.read()
    np_arr = np.frombuffer(content, np.uint8)

    if with_alpha:
        img = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
    else:
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return img
