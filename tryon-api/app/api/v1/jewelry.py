from fastapi import APIRouter

router = APIRouter(prefix="/jewelry", tags=["Jewelry"])

JEWELRY_DB = {
    "earrings": [
        {
            "id": "ear_01",
            "type": "earring",
            "anchor": "ear_lobe",
            "scale": 0.4,
            "offset": { "x": 0, "y": 8 },
            "asset": "/assets/earrings/e.png"
        }
    ],
    "necklace": [
        {
            "id": "neck_01",
            "type": "necklace",
            "anchor": "chin",
            "scale": 0.6,
            "offset": { "x": 0, "y": 90 },
            "asset": "/assets/necklace/n.png"
        }
    ],
    "ring": [
        {
            "id": "ring_01",
            "type": "ring",
            "anchor": "ring_finger",
            "scale": 1.0,
            "offset": { "x": 0, "y": 0 },
            "asset": "/assets/ring/r.png"
        }
    ],
    "bracelet": [
        {
            "id": "brace_01",
            "type": "bracelet",
            "anchor": "wrist",
            "scale": 0.5,
            "offset": { "x": 0, "y": 0 },
            "asset": "/assets/bracelet/b.png"
        }
    ]
}

@router.get("/{type}")
def get_jewelry(type: str):
    return JEWELRY_DB.get(type, [])
