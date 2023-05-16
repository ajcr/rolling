import datetime as dt

import pytest

from rolling.apply_indexed import ApplyIndexed
from rolling.arithmetic.nunique_indexed import NuniqueIndexed


@pytest.mark.parametrize("word", ["aabbc", "xooxyzzziiismsdd", "jjjjjj", ""])
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5])
def test_rolling_nunique(word, window_size):
    idx = range(len(word))
    got = NuniqueIndexed(idx, word, window_size)
    expected = ApplyIndexed(
        idx, word, window_size, function=lambda x: len(set(x))
    )
    assert list(got) == list(expected)


@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5, 6])
def test_index_date(window_size):
    idx, val = zip(*[
        (dt.datetime(2023,5,1), 'Cat1'),
        (dt.datetime(2023,5,2), 'Cat1'),
        (dt.datetime(2023,5,2), 'Cat2'),
        (dt.datetime(2023,5,3), 'Cat3'),
        (dt.datetime(2023,5,6), 'Cat1'),
    ])

    ws = dt.timedelta(days=window_size)

    got = NuniqueIndexed(idx, val, ws)
    expected = ApplyIndexed(idx, val, ws, function=lambda x: len(set(x)))

    assert list(got) == list(expected)