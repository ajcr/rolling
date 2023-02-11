import pytest

from rolling.apply_pairwise import ApplyPairwise

ARRAY_1 = [3, 6, 5, 8, 1]
ARRAY_2 = [1, 2, 3, 4, 5]


@pytest.mark.parametrize(
    "window_size,expected",
    [
        (6, []),
        (5, [[(3, 1), (6, 2), (5, 3), (8, 4), (1, 5)]]),
        (4, [[(3, 1), (6, 2), (5, 3), (8, 4)], [(6, 2), (5, 3), (8, 4), (1, 5)]]),
        (3, [[(3, 1), (6, 2), (5, 3)], [(6, 2), (5, 3), (8, 4)], [(5, 3), (8, 4), (1, 5)]]),
        (2, [[(3, 1), (6, 2)], [(6, 2), (5, 3)], [(5, 3), (8, 4)], [(8, 4), (1, 5)]]),
        (1, [[(3, 1)], [(6, 2)], [(5, 3)], [(8, 4)], [(1, 5)]]),
    ],
)
def test_rolling_apply_pairwise_fixed(window_size, expected):
    r = ApplyPairwise(ARRAY_1, ARRAY_2, window_size, function=lambda x, y: list(zip(x, y)))
    assert list(r) == expected


@pytest.mark.parametrize(
    "window_size,expected",
    [
        (
            6,
            [
                [(3, 1)],
                [(3, 1), (6, 2)],
                [(3, 1), (6, 2), (5, 3)],
                [(3, 1), (6, 2), (5, 3), (8, 4)],
                [(3, 1), (6, 2), (5, 3), (8, 4), (1, 5)],
            ]
        ),
        (
            5,
            [
                [(3, 1)],
                [(3, 1), (6, 2)],
                [(3, 1), (6, 2), (5, 3)],
                [(3, 1), (6, 2), (5, 3), (8, 4)],
                [(3, 1), (6, 2), (5, 3), (8, 4), (1, 5)],
                [(6, 2), (5, 3), (8, 4), (1, 5)],
                [(5, 3), (8, 4), (1, 5)],
                [(8, 4), (1, 5)],
                [(1, 5)],
            ],
        ),
        (
            4,
            [
                [(3, 1)],
                [(3, 1), (6, 2)],
                [(3, 1), (6, 2), (5, 3)],
                [(3, 1), (6, 2), (5, 3), (8, 4)],
                [(6, 2), (5, 3), (8, 4), (1, 5)],
                [(5, 3), (8, 4), (1, 5)],
                [(8, 4), (1, 5)],
                [(1, 5)],
            ],
        ),
        (
            3,
            [
                [(3, 1)],
                [(3, 1), (6, 2)],
                [(3, 1), (6, 2), (5, 3)],
                [(6, 2), (5, 3), (8, 4)],
                [(5, 3), (8, 4), (1, 5)],
                [(8, 4), (1, 5)],
                [(1, 5)],
            ],
        ),
        (
            2,
            [
                [(3, 1)],
                [(3, 1), (6, 2)],
                [(6, 2), (5, 3)],
                [(5, 3), (8, 4)],
                [(8, 4), (1, 5)],
                [(1, 5)],
            ],
        ),
        (
            1,
            [
                [(3, 1)],
                [(6, 2)],
                [(5, 3)],
                [(8, 4)],
                [(1, 5)],
            ]
        ),
    ],
)
def test_rolling_apply_variable(window_size, expected):
    r = ApplyPairwise(
        ARRAY_1,
        ARRAY_2,
        window_size,
        window_type="variable",
        function=lambda x, y: list(zip(x, y)),
    )
    assert list(r) == expected


@pytest.mark.parametrize(
    "array_1,array_2,window_type,expected",
    [
        ([], [], "fixed", []),
        ([3], [], "fixed", []),
        ([], [5], "fixed", []),
        ([], [], "variable", []),
        ([1], [1], "variable", [[(1, 1)]]),
    ],
)
def test_rolling_apply_pairwise_over_short_iterables(array_1, array_2, window_type, expected):
    r = ApplyPairwise(
        array_1,
        array_2,
        10,
        window_type=window_type,
        function=lambda x, y: list(zip(x, y)),
    )
    assert list(r) == expected
