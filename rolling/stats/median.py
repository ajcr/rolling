from collections import deque
from itertools import islice

from rolling.base import RollingObject
from rolling.structures.skiplist import IndexableSkiplist


class Median(RollingObject):
    """
    Iterator object that computes the median value
    of a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Complexity
    ----------

    Update time:  O(log k)
    Memory usage: O(k)

    where k is the size of the rolling window

    Notes
    -----

    An indexable skiplist is used to track the median
    as the window moves (using an idea of R. Hettinger [1]).

    [1] http://code.activestate.com/recipes/576930/

    """

    def _init_fixed(self, iterable, window_size, **kwargs):
        self._buffer = deque(maxlen=window_size)
        self._skiplist = IndexableSkiplist(window_size)

        # update buffer and skiplist with initial values
        for new in islice(self._iterator, window_size - 1):
            self._add_new(new)

        try:
            # insert a dummy value (the last element seen) so that
            # the window is full and iterator works as expected
            self._buffer.appendleft(new)
            self._skiplist.insert(new)
        except UnboundLocalError:
            # if we didn't see any elements (the iterable had no
            # elements or just one element), just use 0 instead
            self._buffer.appendleft(0)
            self._skiplist.insert(0)

    def _init_variable(self, iterable, window_size, **kwargs):
        self._buffer = deque(maxlen=window_size)
        self._skiplist = IndexableSkiplist(window_size)

    def _update_window(self, new):
        old = self._buffer.popleft()
        self._skiplist.remove(old)
        self._skiplist.insert(new)
        self._buffer.append(new)

    def _add_new(self, new):
        self._skiplist.insert(new)
        self._buffer.append(new)

    def _remove_old(self):
        old = self._buffer.popleft()
        self._skiplist.remove(old)

    @property
    def current_value(self):
        if self._obs % 2 == 1:
            return self._skiplist[self._obs // 2]
        else:
            i = self._obs // 2
            return (self._skiplist[i] + self._skiplist[i - 1]) / 2

    @property
    def _obs(self):
        return len(self._buffer)

