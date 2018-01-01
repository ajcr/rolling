import pytest

from rolling.stats import RollingMean

@pytest.mark.parametrize('array,window_size,expected', [
    ([3, 0, 1, 7, 2], 5, [13/5]),
    ([3, 0, 1, 7, 2], 4, [11/4, 10/4]),
    ([3, 0, 1, 7, 2], 3, [4/3, 8/3, 10/3]),
    ([3, 0, 1, 7, 2], 2, [3/2, 1/2, 8/2, 9/2]),
    ([3, 0, 1, 7, 2], 1, [3, 0, 1, 7, 2]),

    ([3, -8, 1, 7, -2], 5, [1/5]),
    ([3, -8, 1, 7, -2], 4, [3/4, -2/4]),
    ([3, -8, 1, 7, -2], 3, [-4/3, 0/3, 6/3]),
    ([3, -8, 1, 7, -2], 2, [-5/2, -7/2, 8/2, 5/2]),
    ([3, -8, 1, 7, -2], 1, [3, -8, 1, 7, -2]),
])
def test_rolling_mean(array, window_size, expected):
    r = RollingMean(array, window_size)
    assert pytest.approx(list(r)) == expected
