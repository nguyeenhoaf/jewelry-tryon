class EMA:
    def __init__(self, alpha=0.6):
        self.alpha = alpha
        self.prev = None

    def apply(self, current):
        if self.prev is None:
            self.prev = current
        else:
            self.prev = self.alpha * current + (1 - self.alpha) * self.prev
        return self.prev
