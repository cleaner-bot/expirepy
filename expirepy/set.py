from .time import default_time_func, default_time_scale, TimeCallable


class ExpiringSet:
    _dict: dict[str, float]
    expires: float

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

    def add(self, item):
        now = self.time_func()
        self._dict[item] = now

    def clear(self):
        self._dict.clear()

    def copy(self):
        self.evict()
        return set(self._dict.keys())

    def update(self, items):
        now = self.time_func()
        self._dict.update((item, now) for item in items)

    def evict(self):
        now = self.time_func()
        ttl = self.expires * self.time_scale
        # need to make a copy or we'd get errors when modifying the dict
        items = tuple(self._dict.keys())
        for item in items:
            added_to_set = self._dict[item]
            if now - added_to_set >= ttl:
                del self._dict[item]

    def __contains__(self, item):
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
