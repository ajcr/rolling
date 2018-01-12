from collections import Counter, deque
from itertools import islice

from .base import RollingObject


class RollingSum(RollingObject):
    """Iterator object that computes the sum
    of a rolling window over a Python iterable.

    The cost of updating the sum of each new
    window is O(1). The memory used is O(k)
    where k is the size of the window.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Examples
    --------

    >>> seq = (8, 1, 1, 3, 6, 5)
    >>> r_sum = RollingSum(seq, 3)
    >>> next(r_sum)
    10
    >>> next(r_sum)
    5
    >>> r_sum = RollingSum(seq, 4)
    [13, 11, 15]

    Notes
    -----

    This object can also be instantiated using the
    `rolling()` function by passing 'Sum':

    >>> from rolling
    >>> r_sum = rolling(seq, window_size=3, func='Sum')

    """
    _func_name = 'Sum'

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)
        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)
        self._buffer.appendleft(0)
        self._sum = sum(self._buffer)

    def _update(self):
        value = next(self._iterator)
        self._sum += value - self._buffer.popleft()
        self._buffer.append(value)

    def __next__(self):
        self._update()
        return self._sum


# N.B. not currently part of the public API
class RollingNunique(RollingObject):

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)
        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)
        self._counter = Counter(self._buffer)
        self._nunique = len(self._counter)

    def _update(self):
        n = next(self._iterator)
        out = self._buffer.popleft()
        self._counter[out] -= 1
        if self._counter[out] == 0:
            del self._counter[out]

    def __next__(self):
        self._update()
        return len(self._counter)



