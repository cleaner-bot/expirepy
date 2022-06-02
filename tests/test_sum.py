from expirepy import ExpiringSum
from expirepy.time import default_time_func, default_time_scale

from .timehelper import TimeHelper


def test_increase() -> None:
    with TimeHelper() as th:
        es = ExpiringSum(3, **th.args())
        assert es.value() == 0
        es.change(1)
        assert es.value() == 1
        es.change(3)
        assert es.value() == 4
        es.change(-10)
        assert es.value() == -6


def test_expire() -> None:
    with TimeHelper() as th:
        es = ExpiringSum(3, **th.args())
        assert es.value() == 0
        es.change(1)
        th.advance(1)
        assert es.value() == 1
        es.change(1)
        th.advance(1)
        assert es.value() == 2
        es.change(1)
        th.advance(1)
        assert es.value() == 2
        es.change(1)
        th.advance(1)
        assert es.value() == 2
        th.advance(2)
        assert es.value() == 0


def test_default() -> None:
    es = ExpiringSum(3)
    assert es.time_func == default_time_func
    assert es.time_scale == default_time_scale
