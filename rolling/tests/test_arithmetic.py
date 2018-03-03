import pytest

from rolling.arithmetic import Sum, Nunique

@pytest.mark.parametrize('array,window_size,expected', [
    ([3, 0, 1, 7, 2], 6, []),
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

    ([],  5, []),
    ([1], 5, []),
])
def test_rolling_sum(array, window_size, expected):
    r = Sum(array, window_size)
    assert list(r) == expected

@pytest.mark.parametrize('array,window_size,expected', [
    ([3, 0, 1, 7, 2], 5, [3, 3, 4, 11, 13, 10, 10, 9, 2]),
    ([3, 0, 1, 7, 2], 4, [3, 3, 4, 11, 10, 10, 9, 2]),
    ([3, 0, 1, 7, 2], 3, [3, 3, 4, 8, 10, 9, 2]),
    ([3, 0, 1, 7, 2], 2, [3, 3, 1, 8, 9, 2]),
    ([3, 0, 1, 7, 2], 1, [3, 0, 1, 7, 2]),

    ([3, -8, 1, 7, -2], 5, [3, -5, -4, 3, 1, -2, 6, 5, -2]),
    ([3, -8, 1, 7, -2], 4, [3, -5, -4, 3, -2, 6, 5, -2]),
    ([3, -8, 1, 7, -2], 3, [3, -5, -4, 0, 6, 5, -2]),
    ([3, -8, 1, 7, -2], 2, [3, -5, -7, 8, 5, -2]),
    ([3, -8, 1, 7, -2], 1, [3, -8, 1, 7, -2]),

    ([], 5, []),
])
def test_rolling_sum_variable(array, window_size, expected):
    r = Sum(array, window_size, window_type='variable')
    assert list(r) == expected


@pytest.mark.parametrize('word,window_size,expected', [
    ('aabbc', 5, [3]),
    ('aabbc', 4, [2, 3]),
    ('aabbc', 3, [2, 2, 2]),
    ('aabbc', 2, [1, 2, 1, 2]),
    ('aabbc', 1, [1, 1, 1, 1, 1]),

    ('xooxyzzziiismsdd', 9, [5, 5, 5, 5, 5, 4, 5, 5]),
    ('xooxyzzziiismsdd', 6, [4, 4, 4, 4, 3, 2, 3, 4, 3, 4, 4]),
    ('xooxyzzziiismsdd', 4, [2, 3, 4, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3]),

    ([], 5, []),
])
def test_rolling_nunique(word, window_size, expected):
    r = Nunique(word, window_size)
    assert list(r) == expected

@pytest.mark.parametrize('word,window_size,expected', [
    ('aabbc', 5, [1, 1, 2, 2, 3, 3, 2, 2, 1]),
    ('aabbc', 4, [1, 1, 2, 2, 3, 2, 2, 1]),
    ('aabbc', 3, [1, 1, 2, 2, 2, 2, 1]),
    ('aabbc', 2, [1, 1, 2, 1, 2, 1]),
    ('aabbc', 1, [1, 1, 1, 1, 1]),

    ('xooxyzzziiismsdd', 7, [1, 2, 2, 2, 3, 4, 4, 4, 5, 4, 3, 3, 4, 4, 4, 4, 4, 3, 3, 2, 1, 1]),
    ('xooxyzzziiismsdd', 6, [1, 2, 2, 2, 3, 4, 4, 4, 4, 3, 2, 3, 4, 3, 4, 4, 3, 3, 2, 1, 1]),
    ('xooxyzzziiismsdd', 4, [1, 2, 2, 2, 3, 4, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 1, 1]),

    ([], 5, []),
    (['x'], 5, [1]),
])
def test_rolling_nunique_variable(word, window_size, expected):
    r = Nunique(word, window_size, window_type='variable')
    assert list(r) == expected
