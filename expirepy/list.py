from collections import deque
import typing

from .time import default_time_func, default_time_scale, TimeCallable


class ExpiringList:
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

    def append(self, item):
        now = self.time_func()
        self._list.append((now, item))

    def copy(self):
        self.evict()
        return [x[1] for x in self._list]

    def extend(self, items):
        now = self.time_func()
        self._list.extend((now, x) for x in items)

    def clear(self):
        self._list.clear()

    def count(self, item):
        self.evict()
        return sum(1 for x in self._list if x[1] == item)

    def remove(self, item):
        self.evict()
        for exact in self._list:
            if exact[1] == item:
                self._list.remove(exact)
                return

    def evict(self):
        now = self.time_func()
        ttl = self.expires * self.time_scale
        while self._list and now - self._list[0][0] >= ttl:
            self._list.popleft()
