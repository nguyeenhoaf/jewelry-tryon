def to_3d_transform(center, angle, scale):
    return {
        "position": [center[0]/100, -center[1]/100, 0],
        "rotation": [0, 0, angle],
        "scale": scale
    }
