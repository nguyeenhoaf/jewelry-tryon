import base64
from io import BytesIO
from PIL import Image

def decode_base64_image(base64_str: str) -> Image.Image:
    img_bytes = base64.b64decode(base64_str)
    return Image.open(BytesIO(img_bytes)).convert("RGBA")

def encode_base64_image(img: Image.Image) -> str:
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()
