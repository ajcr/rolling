from functools import partial

import pytest

from rolling.apply import Apply
from rolling.similarity import JaccardIndex, jaccard_index


@pytest.mark.parametrize(
    "set_a, set_b, expected",
    [
        # fmt: off
        ({1, 2, 3}, {1, 2, 3},      1),
        ({1, 2, 3}, {1},          1/3),
        ({1, 2, 3}, {1, 2},       2/3),
        ({1, 2, 3}, {0},            0),
        ({1, 2, 3}, {1, 2, 3, 4}, 3/4),
        ({1, 2, 3}, {2, 3, 4},    2/4),
        ({1, 2, 3}, {2, 3, 4, 5}, 2/5),
        # fmt: on
    ],
)
def test_jaccard_index(set_a, set_b, expected):
    assert pytest.approx(jaccard_index(set_a, set_b)) == expected


@pytest.mark.parametrize(
    "sequence",
    [
        [3, 1, 4, 1, 5, 9, 2, 1, 4, 1, 5, 6, 7],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
        [3, 3, 2, 1, 0, 5, 5, 5, 5, 5, 2, 3, 2],
    ],
)
@pytest.mark.parametrize(
    "target_set",
    [
        {0},
        {0, 1},
        {0, 1, 2},
        {0, 1, 2, 3},
        {0, 1, 2, 3, 4},
        {0, 1, 2, 3, 4, 5},
    ],
)
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5, 7])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_jaccard_index(sequence, window_size, window_type, target_set):
    got = JaccardIndex(
        sequence, window_size, window_type=window_type, target_set=target_set,
    )
    func = partial(jaccard_index, target_set)
    expected = Apply(sequence, window_size, operation=func, window_type=window_type)
    assert pytest.approx(list(got)) == list(expected)
