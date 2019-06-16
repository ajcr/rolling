import string

from hypothesis import given, strategies as st
import pytest

from rolling.apply import Apply
from rolling.arithmetic import Sum, Product, Nunique


def _product(it):
    x = 1
    for i in it:
        x *= i
    return x


@given(array=st.lists(st.integers(), max_size=15), window_size=st.integers(1, 15))
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_sum(array, window_size, window_type):
    got = Sum(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=sum, window_type=window_type)
    assert list(got) == list(expected)


@given(array=st.lists(st.integers(), max_size=15), window_size=st.integers(1, 15))
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_product(array, window_size, window_type):
    got = Product(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=_product, window_type=window_type)
    assert list(got) == list(expected)


@given(word=st.text(alphabet=string.ascii_lowercase, max_size=15), window_size=st.integers(1, 15))
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_nunique(word, window_size, window_type):
    got = Nunique(word, window_size, window_type=window_type)
    expected = Apply(word, window_size, operation=lambda x: len(set(x)), window_type=window_type)
    assert list(got) == list(expected)
