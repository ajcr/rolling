from collections import deque
from itertools import islice

from .base import RollingObject


class Apply(RollingObject):
    """
    Iterator object that applies a function to
    a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable
    operation : callable, default sum
        a function, or class implementing a __call__
        method, to be applied to each window

    Complexity
    ----------

    Update time:  operation dependent
    Memory usage: O(k)

    where k is the size of the rolling window

    Examples
    --------

    Rolling sum using builtin sum():

    >>> import rolling
    >>> seq = (8, 1, 1, 3, 6, 5)
    >>> r_sum = rolling.Apply(seq, 3, operation=sum)
    >>> next(r_sum)
    10
    >>> next(r_sum)
    5

    Reverse each window:

    >>> r_rev = rolling.Apply(seq, 4, operation=lambda x: list(reversed(x)))
    >>> list(r_rev)
    [[3, 1, 1, 8],
     [6, 3, 1, 1],
     [5, 6, 3, 1]]

    """

    def _init_fixed(self, iterable, window_size, operation=sum, **kwargs):
        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)
        self._operation = operation

    def _init_variable(self, iterable, window_size, operation=sum, **kwargs):
        self._buffer = deque(maxlen=window_size)
        self._operation = operation

    @property
    def current_value(self):
        return self._operation(self._buffer)

    def _add_new(self, new):
        self._buffer.append(new)

    def _remove_old(self):
        self._buffer.popleft()

    def _update_window(self, new):
        self._buffer.append(new)

    @property
    def _obs(self):
        return len(self._buffer)

    def __repr__(self):
        return "Rolling(operation='{}', window_size={}, window_type='{}')".format(
            self._operation.__name__, self.window_size, self.window_type
        )
