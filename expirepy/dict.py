import typing

from .time import TimeCallable, default_time_func, default_time_scale


class ExpiringDict:
    _dict: dict[typing.Any, tuple[float, typing.Any]]

    def __init__(
        self, expires: float, time_func: TimeCallable = None, time_scale: int = None
    ) -> None:
        self._dict = {}
        self.expires = expires
        if time_func is None:
            self.time_func = default_time_func
            self.time_scale = default_time_scale if time_scale is None else time_scale
        else:
            self.time_func = time_func  # type: ignore
            self.time_scale = 1 if time_scale is None else time_scale

    def __setitem__(self, key, value):
        try:
            now = self._dict[key][0]
        except KeyError:
            now = self.time_func()
        self._dict[key] = (now, value)

    def __getitem__(self, key):
        added_to_set, value = self._dict[key]
        now = self.time_func()
        ttl = self.expires * self.time_scale
        if now - added_to_set >= ttl:
            del self._dict[key]
            raise KeyError(key)
        return value

    def get(self, key, fallback=None):
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

    def ttl(self, key):
        added_to_set = self._dict[key][0]
        now = self.time_func()
        ttl = self.expires * self.time_scale
        if now - added_to_set >= ttl:
            del self._dict[key]
            raise KeyError(key)
        return (ttl - now + added_to_set) / self.time_scale

    def clear(self):
        self._dict.clear()

    def copy(self):
        self.evict()
        return {k: v[1] for k, v in self._dict.items()}

    def update(self, dict: dict):
        now = self.time_func()
        self._dict.update((key, (now, value)) for key, value in dict.items())

    def evict(self):
        now = self.time_func()
        ttl = self.expires * self.time_scale
        # need to make a copy or we'd get errors when modifying the dict
        items = tuple(self._dict.keys())
        for item in items:
            added_to_set = self._dict[item][0]
            if now - added_to_set >= ttl:
                del self._dict[item]

    def __contains__(self, key):
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

    def __delitem__(self, key):
        del self._dict[key]
