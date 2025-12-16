from app.core.insightface_loader import get_face_app

def analyze_face(image):
    app = get_face_app()
    faces = app.get(image)

    if not faces:
        return None

    # Lấy khuôn mặt lớn nhất
    faces.sort(key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]), reverse=True)
    return faces[0]
