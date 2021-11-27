import pytest

from rolling.apply import Apply
from rolling.minmax import Min, Max, MinHeap

test_data = (
    [69, 66, 12, 80, 52, 47, 9, 77, 15, 92, 13, 7, 66, 45, 70, 5, 87],
    [0, 39, 46, 1, 78, 87, 76, 88, 64, 86],
    [3, 0, 1, 7, 2],
    [-8, 1, 7, -8, -9],
    [8, 1, 0, -3, 9],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [3, 3, 3, 3, 3],
    [1],
    [],
)


@pytest.mark.parametrize("array", test_data)
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5, 10])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_min(array, window_size, window_type):
    got = Min(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=min, window_type=window_type)
    assert list(got) == list(expected)


@pytest.mark.parametrize("array", test_data)
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5, 10])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_minheap(array, window_size, window_type):
    got = MinHeap(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=min, window_type=window_type)
    assert list(got) == list(expected)


@pytest.mark.parametrize("array", test_data)
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5, 10])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_max(array, window_size, window_type):
    got = Max(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=max, window_type=window_type)
    assert list(got) == list(expected)
