import typing

T = typing.TypeVar("T", bound="TimeHelper")


class TimeHelper:
    def __init__(self, scale: int = 1) -> None:
        self.value = 0.0
        self.scale = scale

    def time_func(self) -> float:
        return self.value * self.scale

    def advance(self, unit: float) -> None:
        self.value += unit

    def args(self) -> dict[str, typing.Any]:
        return {"time_func": self.time_func, "time_scale": self.scale}

    def __enter__(self: T) -> T:
        self.value = 0
        return self

    def __exit__(
        self, exc_type: typing.Any, exc_value: typing.Any, exc_traceback: typing.Any
    ) -> None:
        pass
