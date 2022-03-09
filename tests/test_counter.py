from expirepy import ExpiringCounter
from expirepy.time import default_time_func, default_time_scale

from .timehelper import TimeHelper


def test_increase():
    with TimeHelper() as th:
        ec = ExpiringCounter(3, **th.args())
        assert ec.value() == 0
        ec.increase()
        assert ec.value() == 1
        ec.increase()
        assert ec.value() == 2
        ec.increase()
        assert ec.value() == 3


def test_expire():
    with TimeHelper() as th:
        ec = ExpiringCounter(3, **th.args())
        assert ec.value() == 0
        ec.increase()
        th.advance(1)
        assert ec.value() == 1
        ec.increase()
        th.advance(1)
        assert ec.value() == 2
        ec.increase()
        th.advance(1)
        assert ec.value() == 2
        ec.increase()
        th.advance(1)
        assert ec.value() == 2
        th.advance(2)
        assert ec.value() == 0


def test_default():
    ec = ExpiringCounter(3)
    assert ec.time_func == default_time_func
    assert ec.time_scale == default_time_scale
