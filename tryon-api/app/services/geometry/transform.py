import math

def calc_transform(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    angle = math.atan2(dy, dx)
    scale = math.sqrt(dx * dx + dy * dy)

    return scale, angle
