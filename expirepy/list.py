import typing
from collections import deque

from .time import TimeCallable, default_time_func, default_time_scale

T = typing.TypeVar("T")


class ExpiringList(typing.Generic[T]):
    _list: deque[tuple[float, T]]

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

    def append(self, item: T) -> None:
        now = self.time_func()
        self._list.append((now, item))

    def copy(self) -> typing.Sequence[T]:
        self.evict()
        return [x[1] for x in self._list]

    def extend(self, items: typing.Iterable[T]) -> None:
        now = self.time_func()
        self._list.extend((now, x) for x in items)

    def clear(self) -> None:
        self._list.clear()

    def count(self, item: T) -> int:
        self.evict()
        return sum(1 for x in self._list if x[1] == item)

    def remove(self, item: T) -> None:
        self.evict()
        for exact in self._list:
            if exact[1] == item:
                self._list.remove(exact)
                return

    def evict(self) -> None:
        now = self.time_func()
        ttl = self.expires * self.time_scale
        while self._list and now - self._list[0][0] >= ttl:
            self._list.popleft()
