import pytest

from rolling.structures.bicounter import BiCounter


@pytest.mark.parametrize(
    "iterable,common_items,largest_count",
    [
        (None, set(), 0),
        ("a", {"a"}, 1),
        ("ab", {"a", "b"}, 1),
        ("aba", {"a"}, 2),
        ("abaa", {"a"}, 3),
        ("ababc", {"a", "b"}, 2),
        ("ababcc", {"a", "b", "c"}, 2),
    ],
)
def test_init(iterable, common_items, largest_count):
    bc = BiCounter(iterable)
    assert bc.get_most_common() == common_items
    assert bc.largest_count == largest_count


@pytest.mark.parametrize(
    "iterable,common_items,largest_count",
    [
        (None, {"a"}, 1),
        ("a", {"a"}, 2),
        ("ab", {"a"}, 2),
        ("aba", {"a"}, 3),
        ("abaa", {"a"}, 4),
        ("ababc", {"a"}, 3),
        ("ababcc", {"a"}, 3),
    ],
)
def test_increment_item_a(iterable, common_items, largest_count):
    bc = BiCounter(iterable)
    bc.increment("a")
    assert bc.get_most_common() == common_items
    assert bc.largest_count == largest_count


@pytest.mark.parametrize(
    "iterable,common_items,largest_count",
    [
        (None, set(), 0),
        ("a", set(), 0),
        ("ab", {"b"}, 1),
        ("aba", {"a", "b"}, 1),
        ("abaa", {"a"}, 2),
        ("ababc", {"b"}, 2),
        ("ababcc", {"b", "c"}, 2),
    ],
)
def test_decrement_item_a(iterable, common_items, largest_count):
    bc = BiCounter(iterable)
    bc.decrement("a")
    assert bc.get_most_common() == common_items
    assert bc.largest_count == largest_count
