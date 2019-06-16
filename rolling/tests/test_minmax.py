from hypothesis import given, strategies as st
import pytest

from rolling.apply import Apply
from rolling.minmax import Min, Max, MinHeap


@given(array=st.lists(st.integers(), max_size=15), window_size=st.integers(1, 15))
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_min(array, window_size, window_type):
    got = Min(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=min, window_type=window_type)
    assert list(got) == list(expected)


@given(array=st.lists(st.integers(), max_size=15), window_size=st.integers(1, 15))
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_minheap(array, window_size, window_type):
    got = MinHeap(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=min, window_type=window_type)
    assert list(got) == list(expected)


@given(array=st.lists(st.integers(), max_size=15), window_size=st.integers(1, 15))
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_max(array, window_size, window_type):
    got = Max(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=max, window_type=window_type)
    assert list(got) == list(expected)
