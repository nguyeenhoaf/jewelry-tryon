from typing import List
import numpy as np

def lm(pt, w, h):
    return np.array([pt.x * w, pt.y * h])

FACE = {
    "LEFT_EAR": [234, 93, 132],
    "RIGHT_EAR": [454, 323, 361],
    "CHIN": 152
}

HAND = {
    "RING_MCP": 13,
    "RING_PIP": 14,
    "RING_DIP": 15,
    "WRIST": 0
}
