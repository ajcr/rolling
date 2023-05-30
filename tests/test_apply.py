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


@pytest.mark.parametrize(
    "index_values", [
        list(
            zip(
                [1, 2, 3, 7, 8, 9, 10, 11],
                [5, 6, 4, 0, 2, 1, 21, 17],
            )
        )
    ],
)
@pytest.mark.parametrize(
    "window_size, expected",
    [
        (1, [[5], [6], [4], [0], [2], [1], [21], [17]]),
        (2, [[5], [5, 6], [6, 4], [0], [0, 2], [2, 1], [1, 21], [21, 17]]),
        (
            5,
            [
                [5],
                [5, 6],
                [5, 6, 4],
                [4, 0],
                [0, 2],
                [0, 2, 1],
                [0, 2, 1, 21],
                [0, 2, 1, 21, 17],
            ]
        ),
        (
            30,
            [
                [5],
                [5, 6],
                [5, 6, 4],
                [5, 6, 4, 0],
                [5, 6, 4, 0, 2],
                [5, 6, 4, 0, 2, 1],
                [5, 6, 4, 0, 2, 1, 21],
                [5, 6, 4, 0, 2, 1, 21, 17],
            ]
        ),
    ],
)
def test_rolling_apply_indexed_window(index_values, window_size, expected):
    r = Apply(index_values, window_size, operation=list, window_type="indexed")
    assert list(r) == expected


@pytest.mark.parametrize(
    "index_values", [
        list(
            zip(
                [1, 2, 2, 2, 7, 8, 8, 10],
                [5, 6, 4, 0, 2, 1, 9, 16],
            )
        )
    ],
)
@pytest.mark.parametrize(
    "window_size, expected",
    [
        (1, [[5], [6], [6, 4], [6, 4, 0], [2], [1], [1, 9], [16]]),
        (3, [[5], [5, 6], [5, 6, 4], [5, 6, 4, 0], [2], [2, 1], [2, 1, 9], [1, 9, 16]]),
    ],
)
def test_rolling_apply_indexed_window_repeated_indices(index_values, window_size, expected):
    r = Apply(index_values, window_size, operation=list, window_type="indexed")
    assert list(r) == expected