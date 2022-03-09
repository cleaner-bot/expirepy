from collections import deque
import typing

from .time import default_time_func, default_time_scale, TimeCallable


class ExpiringCounter:
    _list: typing.Sequence[tuple[float, typing.Any]]

    def __init__(
        self,
        expires: float,
        maxlen: int = None,
        time_func: TimeCallable = None,
        time_scale: int = None,
    ) -> None:
        self._list = deque(maxlen=maxlen)
        self.expires = expires
        if time_func is None:
            self.time_func = default_time_func
            self.time_scale = default_time_scale if time_scale is None else time_scale
        else:
            self.time_func = time_func  # type: ignore
            self.time_scale = 1 if time_scale is None else time_scale

    def increase(self):
        now = self.time_func()
        self._list.append(now)

    def value(self):
        self.evict()
        return len(self._list)

    def evict(self):
        now = self.time_func()
        ttl = self.expires * self.time_scale
        while self._list and now - self._list[0] >= ttl:
            self._list.popleft()


class ExpiringSum:
    _list: typing.Sequence[tuple[float, typing.Any]]

    def __init__(
        self,
        expires: float,
        maxlen: int = None,
        time_func: TimeCallable = None,
        time_scale: int = None,
    ) -> None:
        self._list = deque(maxlen=maxlen)
        self.expires = expires
        if time_func is None:
            self.time_func = default_time_func
            self.time_scale = default_time_scale if time_scale is None else time_scale
        else:
            self.time_func = time_func  # type: ignore
            self.time_scale = 1 if time_scale is None else time_scale

    def change(self, value=1):
        now = self.time_func()
        self._list.append((now, value))

    def value(self):
        self.evict()
        return sum(x[1] for x in self._list)

    def evict(self):
        now = self.time_func()
        ttl = self.expires * self.time_scale
        while self._list and now - self._list[0][0] >= ttl:
            self._list.popleft()
