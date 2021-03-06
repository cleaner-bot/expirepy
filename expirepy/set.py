import typing

from .time import TimeCallable, default_time_func, default_time_scale

T = typing.TypeVar("T")


class ExpiringSet(typing.Generic[T]):
    _dict: dict[T, float]
    expires: float

    def __init__(
        self,
        expires: float,
        time_func: TimeCallable | None = None,
        time_scale: int | None = None,
    ) -> None:
        self._dict = {}
        self.expires = expires
        if time_func is None:
            self.time_func = default_time_func
            self.time_scale = default_time_scale if time_scale is None else time_scale
        else:
            self.time_func = time_func
            self.time_scale = 1 if time_scale is None else time_scale

    def add(self, item: T) -> None:
        now = self.time_func()
        self._dict[item] = now

    def remove(self, item: T) -> None:
        del self._dict[item]

    def clear(self) -> None:
        self._dict.clear()

    def copy(self) -> set[T]:
        self.evict()
        return set(self._dict.keys())

    def update(self, items: typing.Iterable[T]) -> None:
        now = self.time_func()
        self._dict.update((item, now) for item in items)

    def evict(self) -> None:
        now = self.time_func()
        ttl = self.expires * self.time_scale
        # need to make a copy or we'd get errors when modifying the dict
        items = tuple(self._dict.keys())
        for item in items:
            added_to_set = self._dict[item]
            if now - added_to_set >= ttl:
                del self._dict[item]

    def __contains__(self, item: T) -> bool:
        try:
            added_to_set = self._dict[item]
        except KeyError:
            return False
        now = self.time_func()
        ttl = self.expires * self.time_scale
        if now - added_to_set >= ttl:
            del self._dict[item]
            return False
        return True
