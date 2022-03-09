from collections import deque
from itertools import islice

from rolling.base import RollingObject
from rolling.structures.bicounter import BiCounter


class Mode(RollingObject):
    """
    Iterator object that computes the mode
    of a rolling window over a Python iterable.

    IMPORTANT: the return set of modal values may be mutated
    as iteration continues. This means that calling list()
    on the rolling Mode object can lead to incorrect-looking
    results as there may be multiple references to the same set.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable
    return_count : bool, default False
        if True, also return an integer showing the
        count of the most common values

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k)

    where k is the size of the rolling window

    Notes
    -----

    A set of the most common items in the window is
    returned. There can be multiple items in this
    set if items are tied for the most common item.

    This contrasts with Python's statistics module
    where mode() will raise an error if the mode
    is not unique.

    """

    def _init_fixed(self, iterable, window_size, return_count=False, **kwargs):
        self._buffer = deque(maxlen=window_size)
        self.return_count = return_count
        self._bicounter = BiCounter()
        for item in islice(self._iterator, window_size - 1):
            self._add_new(item)

        # insert a value to be removed on the first call to update
        self._buffer.appendleft("DUMMY_VALUE")
        self._bicounter.increment("DUMMY_VALUE")

    def _init_variable(self, iterable, window_size, return_count=False, **kwargs):
        self._buffer = deque(maxlen=window_size)
        self.return_count = return_count
        self._bicounter = BiCounter()

    def _update_window(self, new):
        old = self._buffer.popleft()
        self._bicounter.decrement(old)
        self._bicounter.increment(new)
        self._buffer.append(new)

    def _add_new(self, new):
        self._bicounter.increment(new)
        self._buffer.append(new)

    def _remove_old(self):
        old = self._buffer.popleft()
        self._bicounter.decrement(old)

    @property
    def current_value(self):
        if self.return_count:
            return self._bicounter.get_most_common(), self._bicounter.largest_count
        else:
            return self._bicounter.get_most_common()

    @property
    def _obs(self):
        return len(self._buffer)


