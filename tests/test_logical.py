import pytest

from rolling.logical import All, Any


@pytest.mark.parametrize('array,window_size,expected', [
    ([0, 1, 1, 1, 0], 6, []),
    ([0, 1, 1, 1, 0], 5, [False]),
    ([0, 1, 1, 1, 0], 4, [False, False]),
    ([0, 1, 1, 1, 0], 3, [False, True, False]),
    ([0, 1, 1, 1, 0], 2, [False, True, True, False]),
    ([0, 1, 1, 1, 0], 1, [False, True, True, True, False]),

    ([0, 1, 0, 1, 1], 5, [False]),
    ([0, 1, 0, 1, 1], 4, [False, False]),
    ([0, 1, 0, 1, 1], 3, [False, False, False]),
    ([0, 1, 0, 1, 1], 2, [False, False, False, True]),
    ([0, 1, 0, 1, 1], 1, [False, True, False, True, True]),

    ([1, 1, 1, 1, 1], 5, [True]),
    ([1, 1, 1, 1, 1], 4, [True, True]),
    ([1, 1, 1, 1, 1], 3, [True, True, True]),
    ([1, 1, 1, 1, 1], 2, [True, True, True, True]),
    ([1, 1, 1, 1, 1], 1, [True, True, True, True, True]),

    ([],  5, []),
    ([1], 5, []),
])
def test_rolling_all(array, window_size, expected):
    r = All(array, window_size)
    assert list(r) == expected

@pytest.mark.parametrize('array,window_size,expected', [
    ([0, 1, 1, 1, 0], 5, [False, False, False, False, False, False, False, False, False]),
    ([0, 1, 1, 1, 0], 4, [False, False, False, False, False, False, False, False]),
    ([0, 1, 1, 1, 0], 3, [False, False, False, True, False, False, False]),
    ([0, 1, 1, 1, 0], 2, [False, False, True, True, False, False]),
    ([0, 1, 1, 1, 0], 1, [False, True, True, True, False]),

    ([0, 1, 0, 1, 1], 5, [False, False, False, False, False, False, False, True, True]),
    ([0, 1, 0, 1, 1], 4, [False, False, False, False, False, False, True, True]),
    ([0, 1, 0, 1, 1], 3, [False, False, False, False, False, True, True]),
    ([0, 1, 0, 1, 1], 2, [False, False, False, False, True, True]),
    ([0, 1, 0, 1, 1], 1, [False, True, False, True, True]),

    ([1, 1, 1, 1, 1], 5, [True, True, True, True, True, True, True, True, True]),
    ([1, 1, 1, 1, 1], 4, [True, True, True, True, True, True, True, True]),
    ([1, 1, 1, 1, 1], 3, [True, True, True, True, True, True, True]),
    ([1, 1, 1, 1, 1], 2, [True, True, True, True, True, True]),
    ([1, 1, 1, 1, 1], 1, [True, True, True, True, True]),

    ([], 5, []),
])
def test_rolling_all_variable(array, window_size, expected):
    r = All(array, window_size, window_type='variable')
    assert list(r) == expected

@pytest.mark.parametrize('array,window_size,expected', [
    ([0, 1, 1, 1, 0], 6, []),
    ([0, 1, 1, 1, 0], 5, [True]),
    ([0, 1, 1, 1, 0], 4, [True, True]),
    ([0, 1, 1, 1, 0], 3, [True, True, True]),
    ([0, 1, 1, 1, 0], 2, [True, True, True, True]),
    ([0, 1, 1, 1, 0], 1, [False, True, True, True, False]),

    ([0, 0, 0, 1, 1], 5, [True]),
    ([0, 0, 0, 1, 1], 4, [True, True]),
    ([0, 0, 0, 1, 1], 3, [False, True, True]),
    ([0, 0, 0, 1, 1], 2, [False, False, True, True]),
    ([0, 0, 0, 1, 1], 1, [False, False, False, True, True]),

    ([1, 1, 1, 1, 1], 5, [True]),
    ([1, 1, 1, 1, 1], 4, [True, True]),
    ([1, 1, 1, 1, 1], 3, [True, True, True]),
    ([1, 1, 1, 1, 1], 2, [True, True, True, True]),
    ([1, 1, 1, 1, 1], 1, [True, True, True, True, True]),

    ([0, 1, 0, 0, 0], 5, [True]),
    ([0, 1, 0, 0, 0], 4, [True, True]),
    ([0, 1, 0, 0, 0], 3, [True, True, False]),
    ([0, 1, 0, 0, 0], 2, [True, True, False, False]),
    ([0, 1, 0, 0, 0], 1, [False, True, False, False, False]),

    ([],  5, []),
    ([1], 5, []),
])
def test_rolling_any(array, window_size, expected):
    r = Any(array, window_size)
    assert list(r) == expected

@pytest.mark.parametrize('array,window_size,expected', [
    ([0, 0, 0, 1, 1], 5, [False, False, False, True, True, True, True, True, True]),
    ([0, 0, 0, 1, 1], 4, [False, False, False, True, True, True, True, True]),
    ([0, 0, 0, 1, 1], 3, [False, False, False, True, True, True, True]),
    ([0, 0, 0, 1, 1], 2, [False, False, False, True, True, True]),
    ([0, 0, 0, 1, 1], 1, [False, False, False, True, True]),

    ([1, 1, 1, 1, 1], 5, [True, True, True, True, True, True, True, True, True]),
    ([1, 1, 1, 1, 1], 4, [True, True, True, True, True, True, True, True]),
    ([1, 1, 1, 1, 1], 3, [True, True, True, True, True, True, True]),
    ([1, 1, 1, 1, 1], 2, [True, True, True, True, True, True]),
    ([1, 1, 1, 1, 1], 1, [True, True, True, True, True]),

    ([0, 1, 0, 0, 0], 5, [False, True, True, True, True, True, False, False, False]),
    ([0, 1, 0, 0, 0], 4, [False, True, True, True, True, False, False, False]),
    ([0, 1, 0, 0, 0], 3, [False, True, True, True, False, False, False]),
    ([0, 1, 0, 0, 0], 2, [False, True, True, False, False, False]),
    ([0, 1, 0, 0, 0], 1, [False, True, False, False, False]),

    ([1, 0, 0, 1, 0, 0], 5, [True, True, True, True, True, True, True, True, False, False]),
    ([1, 0, 0, 1, 0, 0], 4, [True, True, True, True, True, True, True, False, False]),
    ([1, 0, 0, 1, 0, 0], 3, [True, True, True, True, True, True, False, False]),
    ([1, 0, 0, 1, 0, 0], 2, [True, True, False, True, True, False, False]),
    ([1, 0, 0, 1, 0, 0], 1, [True, False, False, True, False, False]),

    ([], 5, []),
])
def test_rolling_any_variable(array, window_size, expected):
    r = Any(array, window_size, window_type='variable')
    assert list(r) == expected
