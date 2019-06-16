from hypothesis import given, strategies as st
import pytest

from rolling.apply import Apply
from rolling.logical import All, Any


@given(array=st.lists(st.booleans(), max_size=15), window_size=st.integers(1, 15))
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_all(array, window_size, window_type):
    got = All(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=all, window_type=window_type)
    assert list(got) == list(expected)


@given(array=st.lists(st.booleans(), max_size=15), window_size=st.integers(1, 15))
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_any(array, window_size, window_type):
    got = Any(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=any, window_type=window_type)
    assert list(got) == list(expected)
