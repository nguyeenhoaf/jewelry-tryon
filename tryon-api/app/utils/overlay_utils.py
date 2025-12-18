def overlay_rgba(bg, fg, x, y):
    h, w = fg.shape[:2]
    bg_h, bg_w = bg.shape[:2]

    if x < 0 or y < 0 or x + w > bg_w or y + h > bg_h:
        return bg

    alpha = fg[:, :, 3] / 255.0
    alpha_inv = 1.0 - alpha

    for c in range(0, 3):
        bg[y:y+h, x:x+w, c] = (alpha * fg[:, :, c] + alpha_inv * bg[y:y+h, x:x+w, c])

    return bg