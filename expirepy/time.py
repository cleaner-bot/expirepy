import time
import typing


TimeCallable = typing.Callable[[], float]


if hasattr(time, "monotonic_ns"):  # pragma: no cover
    default_time_func = time.monotonic_ns
    default_time_scale = 1_000_000_000
else:  # pragma: no cover
    default_time_func = time.monotonic  # type: ignore
    default_time_scale = 1
