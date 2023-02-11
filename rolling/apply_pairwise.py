from collections import deque
from itertools import islice

from .base_pairwise import RollingPairwise


class ApplyPairwise(RollingPairwise):
    """
    Apply a binary function to windows over two iterables.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable
    function : callable,
        a binary callable to be applied to the current
        window of each iterable

    Complexity
    ----------

    Update time:  function dependent
    Memory usage: O(k)

    where k is the size of the rolling window

    Example
    --------

    >>> from rolling import ApplyPairwise
    >>> from statistics import correlation
    >>> seq_1 = [1, 2, 3, 4, 5]
    >>> seq_2 = [1, 2, 3, 2, 1]
    >>> r_corr = ApplyPairwise(seq_1, seq_2, window_size=3, function=correlation)
    >>> list(r_corr)
    [1.0, 0.0, -1.0]

    """
    def __init__(self, iterable_1, iterable_2, window_size, function, window_type="fixed"):
        self._buffer_1 = deque(maxlen=window_size)
        self._buffer_2 = deque(maxlen=window_size)
        self._function = function
        super().__init__(iterable_1, iterable_2, window_size=window_size, window_type=window_type)

    def _init_fixed(self, **kwargs):
        pairs = zip(self._iterator_1, self._iterator_2)
        for item_1, item_2 in islice(pairs, self.window_size-1):
            self._buffer_1.append(item_1)
            self._buffer_2.append(item_2)

    def _init_variable(self, **kwargs):
        pass # no action required

    @property
    def current_value(self):
        return self._function(self._buffer_1, self._buffer_2)

    def _add_new(self, new_1, new_2):
        self._buffer_1.append(new_1)
        self._buffer_2.append(new_2)

    def _remove_old(self):
        self._buffer_1.popleft()
        self._buffer_2.popleft()

    def _update_window(self, new_1, new_2):
        self._buffer_1.append(new_1)
        self._buffer_2.append(new_2)

    @property
    def _obs(self):
        return len(self._buffer_1)

    def __repr__(self):
        return "RollingPairwise(operation='{}', window_size={}, window_type='{}')".format(
            self._function.__name__, self.window_size, self.window_type
        )
