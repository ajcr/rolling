import pytest

from rolling.structures.sortedlist import SortedList


def test_sortedlist():

    sortedlist = SortedList()
    assert sortedlist._list == []

    with pytest.raises(ValueError):
        sortedlist.remove(12345)

    sortedlist.insert(3)
    assert sortedlist._list == [3]

    sortedlist.insert(2)
    assert sortedlist._list == [2, 3]

    sortedlist.insert(2)
    assert sortedlist._list == [2, 2, 3]

    sortedlist.insert(5)
    assert sortedlist._list == [2, 2, 3, 5]

    sortedlist.insert(4)
    assert sortedlist._list == [2, 2, 3, 4, 5]

    with pytest.raises(ValueError):
        sortedlist.remove(999)

    sortedlist.remove(3)
    assert sortedlist._list == [2, 2, 4, 5]

    sortedlist.remove(2)
    assert sortedlist._list == [2, 4, 5]

    sortedlist.remove(5)
    assert sortedlist._list == [2, 4]

    sortedlist.remove(2)
    assert sortedlist._list == [4]

    sortedlist.remove(4)
    assert sortedlist._list == []
