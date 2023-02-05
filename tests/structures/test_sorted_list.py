import pytest

from rolling.structures.sorted_list import SortedList


def test_sorted_list():

    sorted_list = SortedList()
    assert sorted_list == []

    with pytest.raises(ValueError):
        sorted_list.remove(12345)

    sorted_list.insert(3)
    assert sorted_list == [3]

    sorted_list.insert(2)
    assert sorted_list == [2, 3]

    sorted_list.insert(2)
    assert sorted_list == [2, 2, 3]

    sorted_list.insert(5)
    assert sorted_list == [2, 2, 3, 5]

    sorted_list.insert(4)
    assert sorted_list == [2, 2, 3, 4, 5]

    with pytest.raises(ValueError):
        sorted_list.remove(999)

    sorted_list.remove(3)
    assert sorted_list == [2, 2, 4, 5]

    sorted_list.remove(2)
    assert sorted_list == [2, 4, 5]

    sorted_list.remove(5)
    assert sorted_list == [2, 4]

    sorted_list.remove(2)
    assert sorted_list == [4]

    sorted_list.remove(4)
    assert sorted_list == []
