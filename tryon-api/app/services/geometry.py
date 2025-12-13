import numpy as np
import math

def midpoint(p1, p2):
    return (p1 + p2) / 2

def distance(p1, p2):
    return np.linalg.norm(p2 - p1)

def angle_deg(p1, p2):
    return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))

def clamp(val, min_v, max_v):
    return max(min(val, max_v), min_v)
