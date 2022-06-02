from expirepy import ExpiringList
from expirepy.time import default_time_func, default_time_scale

from .timehelper import TimeHelper


def test_append() -> None:
    with TimeHelper() as th:
        el: ExpiringList[str] = ExpiringList(3, **th.args())
        el.append("foo")
        el.append("bar")
        assert el.copy() == ["foo", "bar"]


def test_extend() -> None:
    with TimeHelper() as th:
        el: ExpiringList[str] = ExpiringList(3, **th.args())
        el.extend(["foo", "bar"])
        assert el.copy() == ["foo", "bar"]
        el.extend(map(str, range(5)))
        assert el.copy() == ["foo", "bar", 0, 1, 2, 3, 4]


def test_clear() -> None:
    with TimeHelper() as th:
        el: ExpiringList[str] = ExpiringList(3, **th.args())
        assert len(el.copy()) == 0
        el.extend(map(str, range(100)))
        assert len(el.copy()) == 100
        el.clear()
        assert len(el.copy()) == 0


def test_expire() -> None:
    with TimeHelper() as th:
        el: ExpiringList[str] = ExpiringList(3, **th.args())
        el.append("foo")
        el.append("bar")
        assert el.copy() == ["foo", "bar"]
        th.advance(1)
        assert el.copy() == ["foo", "bar"]
        th.advance(1)
        assert el.copy() == ["foo", "bar"]
        th.advance(1)
        assert el.copy() == []


def test_count() -> None:
    with TimeHelper() as th:
        el: ExpiringList[str] = ExpiringList(3, **th.args())
        el.append("foo")
        el.append("bar")
        assert el.count("foo") == 1
        assert el.count("bar") == 1
        th.advance(1)
        for _ in range(10):
            el.append("foo")
        assert el.count("foo") == 11
        th.advance(2)
        assert el.count("foo") == 10
        assert el.count("bar") == 0


def test_remove() -> None:
    with TimeHelper() as th:
        el: ExpiringList[str] = ExpiringList(3, **th.args())
        el.append("foo")
        el.append("bar")
        el.append("foo")
        assert el.copy() == ["foo", "bar", "foo"]
        el.remove("bar")
        assert el.copy() == ["foo", "foo"]


def test_default() -> None:
    el: ExpiringList[str] = ExpiringList(3)
    assert el.time_func == default_time_func
    assert el.time_scale == default_time_scale
