import pytest

from rolling.apply import Apply
from rolling.arithmetic import Sum, Product, Nunique


def _product(it):
    x = 1
    for i in it:
        x *= i
    return x


@pytest.mark.parametrize(
    "array",
    [
        [3, -8, 1, 7, -2, 4, 7, 2, 1],
        [3, -8, 0, 7, -2, 4, 7, 0, 1],
        [3, 0, 1, 7, 2],
        [1],
        [],
    ],
)
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_sum(array, window_size, window_type):
    got = Sum(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=sum, window_type=window_type)
    assert list(got) == list(expected)


@pytest.mark.parametrize(
    "array",
    [
        [3, -8, 1, 7, -2, 4, 7, 2, 1],
        [3, -8, 0, 7, -2, 4, 7, 0, 1],
        [3, 0, 1, 7, 2],
        [1],
        [],
    ],
)
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_product(array, window_size, window_type):
    got = Product(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=_product, window_type=window_type)
    assert list(got) == list(expected)


@pytest.mark.parametrize("word", ["aabbc", "xooxyzzziiismsdd", "jjjjjj", ""])
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_nunique(word, window_size, window_type):
    got = Nunique(word, window_size, window_type=window_type)
    expected = Apply(
        word, window_size, operation=lambda x: len(set(x)), window_type=window_type
    )
    assert list(got) == list(expected)
