import pytest

from rolling.apply import Apply


@pytest.mark.parametrize("array", [[3, 6, 5, 8, 1]])
@pytest.mark.parametrize(
    "window_size,expected",
    [
        (6, []),
        (5, [[3, 6, 5, 8, 1]]),
        (4, [[3, 6, 5, 8], [6, 5, 8, 1]]),
        (3, [[3, 6, 5], [6, 5, 8], [5, 8, 1]]),
        (2, [[3, 6], [6, 5], [5, 8], [8, 1]]),
        (1, [[3], [6], [5], [8], [1]]),
    ],
)
def test_rolling_apply(array, window_size, expected):
    r = Apply(array, window_size, operation=list)
    assert list(r) == expected


@pytest.mark.parametrize("array", [[3, 6, 5, 8, 1]])
@pytest.mark.parametrize(
    "window_size,expected",
    [
        (6, [[3], [3, 6], [3, 6, 5], [3, 6, 5, 8], [3, 6, 5, 8, 1]]),
        (
            5,
            [
                [3],
                [3, 6],
                [3, 6, 5],
                [3, 6, 5, 8],
                [3, 6, 5, 8, 1],
                [6, 5, 8, 1],
                [5, 8, 1],
                [8, 1],
                [1],
            ],
        ),
        (
            4,
            [
                [3],
                [3, 6],
                [3, 6, 5],
                [3, 6, 5, 8],
                [6, 5, 8, 1],
                [5, 8, 1],
                [8, 1],
                [1],
            ],
        ),
        (3, [[3], [3, 6], [3, 6, 5], [6, 5, 8], [5, 8, 1], [8, 1], [1]]),
        (2, [[3], [3, 6], [6, 5], [5, 8], [8, 1], [1]]),
        (1, [[3], [6], [5], [8], [1]]),
    ],
)
def test_rolling_apply_variable(array, window_size, expected):
    r = Apply(array, window_size, operation=list, window_type="variable")
    assert list(r) == expected


@pytest.mark.parametrize(
    "array,window_type,expected",
    [
        ([], "fixed", []),
        ([3], "fixed", []),
        ([], "variable", []),
        ([1], "variable", [[1]]),
    ],
)
def test_rolling_apply_over_short_iterable(array, window_type, expected):
    r = Apply(array, 5, operation=list, window_type=window_type)
    assert list(r) == expected
