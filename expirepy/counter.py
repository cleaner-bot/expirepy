import typing
from collections import deque

from .time import TimeCallable, default_time_func, default_time_scale


class ExpiringCounter:
    _list: deque[float]

    def __init__(
        self,
        expires: float,
        maxlen: int | None = None,
        time_func: TimeCallable | None = None,
        time_scale: int | None = None,
    ) -> None:
        self._list = deque(maxlen=maxlen)
        self.expires = expires
        if time_func is None:
            self.time_func = default_time_func
            self.time_scale = default_time_scale if time_scale is None else time_scale
        else:
            self.time_func = time_func
            self.time_scale = 1 if time_scale is None else time_scale

    def increase(self) -> None:
        now = self.time_func()
        self._list.append(now)

    def value(self) -> int:
        self.evict()
        return len(self._list)

    def evict(self) -> None:
        now = self.time_func()
        ttl = self.expires * self.time_scale
        while self._list and now - self._list[0] >= ttl:
            self._list.popleft()


class ExpiringSum:
    _list: deque[tuple[float, typing.Any]]

    def __init__(
        self,
        expires: float,
        maxlen: int | None = None,
        time_func: TimeCallable | None = None,
        time_scale: int | None = None,
    ) -> None:
        self._list = deque(maxlen=maxlen)
        self.expires = expires
        if time_func is None:
            self.time_func = default_time_func
            self.time_scale = default_time_scale if time_scale is None else time_scale
        else:
            self.time_func = time_func
            self.time_scale = 1 if time_scale is None else time_scale

    def change(self, value: float = 1) -> None:
        now = self.time_func()
        self._list.append((now, value))

    def value(self) -> float:
        self.evict()
        return sum(x[1] for x in self._list)

    def evict(self) -> None:
        now = self.time_func()
        ttl = self.expires * self.time_scale
        while self._list and now - self._list[0][0] >= ttl:
            self._list.popleft()
