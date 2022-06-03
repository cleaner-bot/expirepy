import typing

from .time import TimeCallable, default_time_func, default_time_scale

T = typing.TypeVar("T")
TK = typing.TypeVar("TK")
TV = typing.TypeVar("TV")


class ExpiringDict(typing.Generic[TK, TV]):
    _dict: dict[TK, tuple[float, TV]]

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

    def __setitem__(self, key: TK, value: TV) -> None:
        try:
            now = self._dict[key][0]
        except KeyError:
            now = self.time_func()
        self._dict[key] = (now, value)

    def __getitem__(self, key: TK) -> TV:
        added_to_set, value = self._dict[key]
        now = self.time_func()
        ttl = self.expires * self.time_scale
        if now - added_to_set >= ttl:
            del self._dict[key]
            raise KeyError(key)
        return value

    @typing.overload
    def get(self, key: TK) -> TV | None:
        ...

    @typing.overload
    def get(self, key: TK, fallback: T) -> TV | T:
        ...

    def get(self, key: TK, fallback: T | None = None) -> TV | T | None:
        try:
            added_to_set, value = self._dict[key]
        except KeyError:
            return fallback
        now = self.time_func()
        ttl = self.expires * self.time_scale
        if now - added_to_set >= ttl:
            del self._dict[key]
            return fallback
        return value

    def ttl(self, key: TK) -> float:
        added_to_set = self._dict[key][0]
        now = self.time_func()
        ttl = self.expires * self.time_scale
        if now - added_to_set >= ttl:
            del self._dict[key]
            raise KeyError(key)
        return (ttl - now + added_to_set) / self.time_scale

    def clear(self) -> None:
        self._dict.clear()

    def copy(self) -> dict[TK, TV]:
        self.evict()
        return {k: v[1] for k, v in self._dict.items()}

    def update(self, dict: dict[TK, TV]) -> None:
        now = self.time_func()
        self._dict.update((key, (now, value)) for key, value in dict.items())

    def evict(self) -> None:
        now = self.time_func()
        ttl = self.expires * self.time_scale
        # need to make a copy or we'd get errors when modifying the dict
        items = tuple(self._dict.keys())
        for item in items:
            added_to_set = self._dict[item][0]
            if now - added_to_set >= ttl:
                del self._dict[item]

    def __contains__(self, key: TK) -> bool:
        try:
            added_to_set = self._dict[key][0]
        except KeyError:
            return False
        now = self.time_func()
        ttl = self.expires * self.time_scale
        if now - added_to_set >= ttl:
            del self._dict[key]
            return False
        return True

    def __delitem__(self, key: TK) -> None:
        del self._dict[key]
