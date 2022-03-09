from expirepy import ExpiringDict
from expirepy.time import default_time_func, default_time_scale
import pytest

from .timehelper import TimeHelper


def test_set():
    with TimeHelper() as th:
        ed = ExpiringDict(3, **th.args())
        ed["foo"] = "bar"
        ed["bar"] = "foo"
        assert ed.copy() == {"foo": "bar", "bar": "foo"}


def test_update():
    with TimeHelper() as th:
        ed = ExpiringDict(3, **th.args())
        assert ed.copy() == {}
        ed.update({"foo": "bar", "bar": "foo"})
        assert ed.copy() == {"foo": "bar", "bar": "foo"}


def test_get():
    with TimeHelper() as th:
        ed = ExpiringDict(3, **th.args())
        ed.update({"foo": "bar", "bar": "foo"})
        assert ed["foo"] == "bar"
        assert ed.get("bar") == "foo"
        assert ed.get("test") is None
        with pytest.raises(KeyError):
            ed["test"]


def test_expire():
    with TimeHelper() as th:
        ed = ExpiringDict(3, **th.args())
        ed["foo"] = "bar"
        ed["bar"] = "foo"
        assert ed.copy() == {"foo": "bar", "bar": "foo"}
        th.advance(2)
        assert ed.copy() == {"foo": "bar", "bar": "foo"}
        ed["test"] = "123"
        assert ed.copy() == {"foo": "bar", "bar": "foo", "test": "123"}
        th.advance(1)
        with pytest.raises(KeyError):
            assert ed["foo"]
        assert ed.get("bar") is None
        assert ed.copy() == {"test": "123"}
        th.advance(2)
        assert ed.copy() == {}


def test_clear():
    with TimeHelper() as th:
        ed = ExpiringDict(3, **th.args())
        ed["foo"] = "bar"
        ed["bar"] = "foo"
        assert ed.copy() == {"foo": "bar", "bar": "foo"}
        ed.clear()
        assert ed.copy() == {}


def test_contains():
    with TimeHelper() as th:
        ed = ExpiringDict(3, **th.args())
        ed["foo"] = "bar"
        assert "foo" in ed
        assert "bar" not in ed
        th.advance(3)
        assert "foo" not in ed


def test_delete():
    with TimeHelper() as th:
        ed = ExpiringDict(3, **th.args())
        ed["foo"] = "bar"
        ed["bar"] = "foo"
        assert ed.copy() == {"foo": "bar", "bar": "foo"}
        del ed["foo"]
        assert ed.copy() == {"bar": "foo"}


def test_ttl():
    with TimeHelper() as th:
        ed = ExpiringDict(3, **th.args())
        ed["foo"] = "bar"
        assert ed.ttl("foo") == 3
        th.advance(1)
        assert ed.ttl("foo") == 2
        th.advance(1)
        assert ed.ttl("foo") == 1
        th.advance(1)
        with pytest.raises(KeyError):
            ed.ttl("foo")


def test_default():
    ed = ExpiringDict(3)
    assert ed.time_func == default_time_func
    assert ed.time_scale == default_time_scale
