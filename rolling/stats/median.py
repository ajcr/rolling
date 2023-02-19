from collections import deque
from itertools import islice

from rolling.base import RollingObject
from rolling.structures.skiplist import IndexableSkiplist
from rolling.structures.sortedlist import SortedList


class Median(RollingObject):
    """
    Median value of a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable
    window_type : 'fixed' (default) or 'variable'
    tracker : 'sortedlist' (default) or 'skiplist'
        data structure used to track the order of the window values

    Complexity
    ----------

    For 'sortedlist' tracker:

        Update time:  O(k)
        Memory usage: O(k)

    For 'skiplist' tracker:

        Update time:  O(log k)
        Memory usage: O(k)

    where k is the size of the rolling window.

    Note that the 'sortedlist' tracker may be faster for smaller
    window sizes due to the overhead of skiplist operations.

    Notes
    -----

    The indexable skiplist to track the median uses an idea and
    code of R. Hettinger [1].

    [1] http://code.activestate.com/recipes/576930/

    """
    def __init__(
        self,
        iterable,
        window_size,
        window_type="fixed",
        tracker="sortedlist",
    ):

        self._buffer = deque(maxlen=window_size)

        if tracker == "skiplist":
            self._tracker = IndexableSkiplist(window_size)
        elif tracker == "sortedlist":
            self._tracker = SortedList()
        else:
            raise ValueError(f"tracker must be one of 'skiplist' or 'sortedlist'")

        super().__init__(iterable, window_size, window_type)

    def _init_fixed(self, iterable, window_size, **kwargs):
        # update buffer and skiplist with initial values
        for new in islice(self._iterator, window_size - 1):
            self._add_new(new)

        try:
            # insert a dummy value (the last element seen) so that
            # the window is full and iterator works as expected
            self._buffer.appendleft(new)
            self._tracker.insert(new)
        except UnboundLocalError:
            # if we didn't see any elements (the iterable had no
            # elements or just one element), just use 0 instead
            self._buffer.appendleft(0)
            self._tracker.insert(0)

    def _init_variable(self, iterable, window_size, **kwargs):
        # no further initialisation required for variable-size windows
        pass

    def _update_window(self, new):
        old = self._buffer.popleft()
        self._tracker.remove(old)
        self._tracker.insert(new)
        self._buffer.append(new)

    def _add_new(self, new):
        self._tracker.insert(new)
        self._buffer.append(new)

    def _remove_old(self):
        old = self._buffer.popleft()
        self._tracker.remove(old)

    @property
    def current_value(self):
        if self._obs % 2 == 1:
            return self._tracker[self._obs // 2]
        else:
            i = self._obs // 2
            return (self._tracker[i] + self._tracker[i - 1]) / 2

    @property
    def _obs(self):
        return len(self._buffer)

