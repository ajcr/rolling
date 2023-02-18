import pytest

from rolling.apply import Apply
from rolling.monotonic import Monotonic


def is_increasing(window):
    seq = list(window)
    return all(a <= b for a, b in zip(seq, seq[1:]))

def is_strictly_increasing(window):
    seq = list(window)
    return all(a < b for a, b in zip(seq, seq[1:]))

def is_decreasing(window):
    seq = list(window)
    return all(a >= b for a, b in zip(seq, seq[1:]))

def is_strictly_decreasing(window):
    seq = list(window)
    return all(a > b for a, b in zip(seq, seq[1:]))


TEST_APPLY_FUNC = {
    # (increasing, strict): test func
    (True, True): is_strictly_increasing,
    (True, False): is_increasing,
    (False, True): is_strictly_decreasing,
    (False, False): is_decreasing
}


TEST_DATA = [
    [0, 1, 3, 7, 11, 15, 21, 11, 2, 1, 3, 5, 7, 4, 2, 1, 9, 10],
    [999, 3, 3, 3, 131, 100, 99, 99, 99, 15, 21, 11, 2, 1, 3, 5, 7, 4, 2, 1, 9, 10],
    list(range(20)),
    list(reversed(range(20))),
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 5, 5, 5, 0, 3, 3, 3, 3, 3, 3, 3],
    [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
    [1, 2, 5, 1, 0, 1, 2, 0, 0, 1, 2, 4, 7, 6, 5, 3, 2, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [1],
    [0],
    [],
]


@pytest.mark.parametrize("array", TEST_DATA)
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
@pytest.mark.parametrize("increasing", [False, True])
@pytest.mark.parametrize("strict", [False, True])
def test_rolling_monotonic(array, window_size, window_type, increasing, strict):
    got = Monotonic(
        array,
        window_size,
        window_type=window_type,
        increasing=increasing,
        strict=strict,
    )

    expected = Apply(
        array,
        window_size,
        operation=TEST_APPLY_FUNC[(increasing, strict)],
        window_type=window_type,
    )

    assert list(got) == list(expected)
