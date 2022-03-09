from expirepy import ExpiringSet
from expirepy.time import default_time_func, default_time_scale

from .timehelper import TimeHelper


def test_add():
    with TimeHelper() as th:
        es = ExpiringSet(3, **th.args())
        es.add("foo")
        es.add("bar")
        assert es.copy() == {"foo", "bar"}


def test_update():
    with TimeHelper() as th:
        es = ExpiringSet(3, **th.args())
        es.update(["foo", "bar"])
        assert es.copy() == {"foo", "bar"}
        es.update(range(5))
        assert es.copy() == {"foo", "bar", 0, 1, 2, 3, 4}


def test_contains():
    with TimeHelper() as th:
        es = ExpiringSet(3, **th.args())
        es.update(["foo", "bar"])

        assert "foo" in es
        assert "bar" in es
        assert "foobar" not in es
        th.advance(3)
        assert "foo" not in es


def test_clear():
    with TimeHelper() as th:
        es = ExpiringSet(3, **th.args())
        es.update(["foo", "bar"])
        assert es.copy() == {"foo", "bar"}
        es.clear()
        assert es.copy() == set()


def test_expire():
    with TimeHelper() as th:
        es = ExpiringSet(3, **th.args())
        es.add("foo")
        es.add("bar")
        assert es.copy() == {"foo", "bar"}
        th.advance(1)
        assert es.copy() == {"foo", "bar"}
        th.advance(1)
        assert es.copy() == {"foo", "bar"}
        th.advance(1)
        assert es.copy() == set()


def test_default():
    es = ExpiringSet(3)
    assert es.time_func == default_time_func
    assert es.time_scale == default_time_scale
