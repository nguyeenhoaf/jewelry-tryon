from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Landmark(BaseModel):
    x: float
    y: float
    z: Optional[float] = 0.0

class TryOnRequest(BaseModel):
    imageBase64: str
    faceLandmarks: Optional[List[Landmark]]
    handLandmarks: Optional[List[List[Landmark]]]
    jewelry: Dict[str, Optional[str]]
