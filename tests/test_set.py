import pytest

from expirepy import ExpiringSet
from expirepy.time import default_time_func, default_time_scale

from .timehelper import TimeHelper


def test_add() -> None:
    with TimeHelper() as th:
        es: ExpiringSet[str] = ExpiringSet(3, **th.args())
        es.add("foo")
        es.add("bar")
        assert es.copy() == {"foo", "bar"}


def test_update() -> None:
    with TimeHelper() as th:
        es: ExpiringSet[str] = ExpiringSet(3, **th.args())
        es.update(["foo", "bar"])
        assert es.copy() == {"foo", "bar"}
        es.update(map(str, range(5)))
        assert es.copy() == {"foo", "bar", "0", "1", "2", "3", "4"}


def test_remove() -> None:
    with TimeHelper() as th:
        es: ExpiringSet[str] = ExpiringSet(3, **th.args())
        es.add("foo")
        es.add("bar")
        es.remove("bar")
        assert es.copy() == {"foo"}
        with pytest.raises(KeyError):
            es.remove("bar")


def test_contains() -> None:
    with TimeHelper() as th:
        es: ExpiringSet[str] = ExpiringSet(3, **th.args())
        es.update(["foo", "bar"])

        assert "foo" in es
        assert "bar" in es
        assert "foobar" not in es
        th.advance(3)
        assert "foo" not in es


def test_clear() -> None:
    with TimeHelper() as th:
        es: ExpiringSet[str] = ExpiringSet(3, **th.args())
        es.update(["foo", "bar"])
        assert es.copy() == {"foo", "bar"}
        es.clear()
        assert es.copy() == set()


def test_expire() -> None:
    with TimeHelper() as th:
        es: ExpiringSet[str] = ExpiringSet(3, **th.args())
        es.add("foo")
        es.add("bar")
        assert es.copy() == {"foo", "bar"}
        th.advance(1)
        assert es.copy() == {"foo", "bar"}
        th.advance(1)
        assert es.copy() == {"foo", "bar"}
        th.advance(1)
        assert es.copy() == set()


def test_default() -> None:
    es: ExpiringSet[str] = ExpiringSet(3)
    assert es.time_func == default_time_func
    assert es.time_scale == default_time_scale
