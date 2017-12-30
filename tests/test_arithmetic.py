import pytest

from rolling.arithmetic import RollingSum

@pytest.mark.parametrize('array,window_size,expected', [
    ([3, 0, 1, 7, 2], 5, [13]),
    ([3, 0, 1, 7, 2], 4, [11, 10]),
    ([3, 0, 1, 7, 2], 3, [4, 8, 10]),
    ([3, 0, 1, 7, 2], 2, [3, 1, 8, 9]),
    ([3, 0, 1, 7, 2], 1, [3, 0, 1, 7, 2]),

    ([3, -8, 1, 7, -2], 5, [1]),
    ([3, -8, 1, 7, -2], 4, [3, -2]),
    ([3, -8, 1, 7, -2], 3, [-4, 0, 6]),
    ([3, -8, 1, 7, -2], 2, [-5, -7, 8, 5]),
    ([3, -8, 1, 7, -2], 1, [3, -8, 1, 7, -2]),
])
def test_rolling_sum(array, window_size, expected):
    r = RollingSum(array, window_size)
    assert list(r) == expected
