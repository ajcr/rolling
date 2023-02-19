import bisect
from typing import MutableSequence


class SortedList(MutableSequence):
    """
    Sorted list with an insert method to maintain order.

    This is a very basic version of SortedContainer's
    SortedList object [1], which uses the Python bisect
    module's bisect/insort methods [2] to efficiently locate
    the correct indices for insertion and removal of values.

    [1] grantjenks.com/docs/sortedcontainers/_modules/sortedcontainers/sortedlist.html#SortedList
    [2] docs.python.org/3/library/bisect.html

    """
    def __init__(self):
        self._list = []

    def remove(self, value):
        index = bisect.bisect_left(self._list, value)
        if index >= len(self) or self._list[index] != value:
            raise ValueError(f"Value not found: {value}")
        self._list.pop(index)

    def insert(self, value):
        bisect.insort(self._list, value)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, value):
        self._list[index] = value

    def __delitem__(self, index):
        del self._list[index]
