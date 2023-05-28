import pytest

from rolling.apply import Apply
from rolling.arithmetic import Sum, Product, Nunique


def _product(it):
    x = 1
    for i in it:
        x *= i
    return x


def _nunique(it):
    return len(set(it))


INDEXED_VALUES = list(
    zip(
        [1, 2, 3, 7, 8, 9, 10, 11, 20],
        [5, 6, 4, 0, 2, 1, 21, 17, 33],
    )
)

INDEXED_VALUES_2 = list(
    zip(
        [1, 2, 3, 7, 8, 9, 10, 11, 20, 23, 24],
        [5, 6, 5, 5, 4, 3,  5,  7,  3,  3,  3],
    )
)


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


@pytest.mark.parametrize("index_values", [INDEXED_VALUES])
@pytest.mark.parametrize("window_size", [1, 3, 5, 7])
def test_rolling_sum_indexed_window(index_values, window_size):
    got = Sum(index_values, window_size, window_type="indexed")
    expected = Apply(index_values, window_size, operation=sum, window_type="indexed")
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


@pytest.mark.parametrize("index_values", [INDEXED_VALUES])
@pytest.mark.parametrize("window_size", [1, 3, 5, 7])
def test_rolling_product_indexed_window(index_values, window_size):
    got = Product(index_values, window_size, window_type="indexed")
    expected = Apply(index_values, window_size, operation=_product, window_type="indexed")
    assert list(got) == list(expected)


@pytest.mark.parametrize("word", ["aabbc", "xooxyzzziiismsdd", "jjjjjj", ""])
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_nunique(word, window_size, window_type):
    got = Nunique(word, window_size, window_type=window_type)
    expected = Apply(word, window_size, operation=_nunique, window_type=window_type)
    assert list(got) == list(expected)


@pytest.mark.parametrize("index_values", [INDEXED_VALUES_2])
@pytest.mark.parametrize("window_size", [1, 3, 5, 7, 10])
def test_rolling_nunique_indexed_window(index_values, window_size):
    got = Nunique(index_values, window_size, window_type="indexed")
    expected = Apply(index_values, window_size, operation=_nunique, window_type="indexed")
    assert list(got) == list(expected)