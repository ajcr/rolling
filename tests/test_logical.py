import pytest

from rolling.apply import Apply
from rolling.logical import All, Any

test_data = (
    [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [1],
    [0],
    [],
)


@pytest.mark.parametrize("array", test_data)
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_all(array, window_size, window_type):
    got = All(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=all, window_type=window_type)
    assert list(got) == list(expected)


@pytest.mark.parametrize("array", test_data)
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_any(array, window_size, window_type):
    got = Any(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=any, window_type=window_type)
    assert list(got) == list(expected)
