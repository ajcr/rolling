import datetime as dt

import pytest

from rolling.apply_indexed import ApplyIndexed

ARRAY_1 = [1, 2, 3, 4, 5]
IDX_1 = [0,1,2,4,6]

@pytest.mark.parametrize(
    "window_size,expected",
    [
        (1, ARRAY_1),
        (2, [1,3,5,4,5]),
        (3, [1,3,6,7,9]),
        (4, [1,3,6,9,9]),
        (5, [1,3,6,10,12]),
        (6, [1,3,6,10,14]),
        (7, [1,3,6,10,15]),
    ],
)
def test_rolling_apply_indexed(window_size, expected):
    r = ApplyIndexed(IDX_1, ARRAY_1, window_size, function=sum)
    assert list(r) == expected

    # Now with datetime
    idx_datetime = [dt.datetime(2023, 5, x+1) for x in IDX_1]
    ws_timedelta = dt.timedelta(days=window_size)
    r = ApplyIndexed(idx_datetime, ARRAY_1, ws_timedelta, function=sum)
    assert list(r) == expected

ARRAY_2 = [1,2,3,4,5,6]
IDX_2 = [0,0,1,2,4,6]

@pytest.mark.parametrize(
    "window_size,expected",
    [
        (1, [1,3,3,4,5,6]),
        (2, [1,3,6,7,5,6]),
    ]
)
def test_rolling_apply_repeated(window_size, expected):
    r = ApplyIndexed(IDX_2, ARRAY_2, window_size, function=sum)
    assert list(r) == expected
