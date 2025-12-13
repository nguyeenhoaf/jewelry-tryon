from pydantic import BaseModel

class TryOnResponse(BaseModel):
    resultImage: str
    width: int
    height: int
