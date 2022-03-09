class TimeHelper:
    def __init__(self, scale: int = 1) -> None:
        self.value = 0
        self.scale = scale

    def time_func(self):
        return self.value * self.scale

    def advance(self, unit):
        self.value += unit

    def args(self):
        return {"time_func": self.time_func, "time_scale": self.scale}

    def __enter__(self):
        self.value = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
