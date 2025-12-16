def overlay_rgba(bg, fg, x, y):
    h, w = fg.shape[:2]

    if x < 0 or y < 0 or x + w > bg.shape[1] or y + h > bg.shape[0]:
        return bg

    alpha = fg[:, :, 3] / 255.0
    for c in range(3):
        bg[y:y+h, x:x+w, c] = (
            alpha * fg[:, :, c] +
            (1 - alpha) * bg[y:y+h, x:x+w, c]
        )
    return bg
