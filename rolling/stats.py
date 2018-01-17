from collections import deque
from itertools import islice
from math import sqrt

from .base import RollingObject
from .arithmetic import RollingSum
from .structures.skiplist import IndexableSkiplist


class RollingMean(RollingSum):
    """Iterator object that computes the mean
    of a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k)

    where k is the size of the rolling window
    """
    _func_name = 'Mean'

    def __next__(self):
        self._update()
        return self._sum / self.window_size


class RollingVar(RollingObject):
    """Iterator object that computes the sample variance
    of a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k)

    where k is the size of the rolling window

    Notes
    -----

    Welford's algorithm is used to compute the variance.
    """
    _func_name = 'Var'

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)

        if window_size <= 1:
            raise ValueError('Window size must be greater than 1')

        self._buffer = deque(maxlen=window_size)

        self._i = 0 # degrees of freedom
        self._mean = 0.0 # mean of values
        self._m2 = 0.0  # sum of squared values less the mean

        for i in range(1, window_size):
            self._i += 1
            self._add_new()

        # insert mean at the start of the buffer so that the
        # the first call to update returns the correct value
        # note: self._i is now (window_size - 1)
        self._buffer.appendleft(self._mean)

    def _add_new(self):
        "Adds a new value to the window"
        new = next(self._iterator)

        delta = new - self._mean
        self._mean += delta / self._i
        self._m2 += delta * (new - self._mean)

        self._buffer.append(new)

    # NOTE: implemented for completeness - not used and untested
    def _remove_old(self):
        "Removes a value from the window"
        old = self._buffer.popleft()

        delta = old - self._mean
        self._mean -= delta / self._i
        self._m2 -= delta * (old - self._mean)

    def _update(self):
        "Adds a new value and removes an old value, maintaining window size"
        new = next(self._iterator)
        old = self._buffer.popleft()

        delta = new - old
        delta_old = old - self._mean
        self._mean += delta / self.window_size
        delta_new = new - self._mean
        self._m2 += delta * (delta_old + delta_new)

        self._buffer.append(new)

    def __next__(self):
        self._update()
        return self._m2 / self._i


class RollingStd(RollingVar):
    """Iterator object that computes the sample standard
    deviation of a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k)

    where k is the size of the rolling window

    Notes
    -----

    Welford's algorithm is used to compute the variance,
    of which the standard deviation is the square root.
    """
    _func_name = 'Std'

    def __next__(self):
        self._update()
        return sqrt(self._m2 / self._i)


class RollingMedian(RollingObject):
    """Iterator object that computes the median value
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
    _func_name = 'Median'

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)
        if window_size <= 1:
            raise ValueError('Window size must be greater than 1')

        self._buffer = deque(maxlen=window_size)
        self._skiplist = IndexableSkiplist(window_size)

        # update buffer and skiplist with initial values
        for value in islice(self._iterator, window_size - 1):
            self._buffer.append(value)
            self._skiplist.insert(value)

        # insert a dummy value (the last element seen) so that
        # the window is full and iterator works as expected
        self._buffer.appendleft(value)
        self._skiplist.insert(value)

        self._median_idx = window_size // 2

        if window_size % 2 == 1:
            self._median_func = self._median_odd
        else:
            self._median_func = self._median_even

    def _update(self):
        new = next(self._iterator)
        old = self._buffer[0]
        self._skiplist.remove(old)
        self._skiplist.insert(new)
        self._buffer.append(new)

    def _median_odd(self):
        i = self._median_idx
        return self._skiplist[i]

    def _median_even(self):
        i = self._median_idx
        return (self._skiplist[i] + self._skiplist[i-1]) / 2

    def __next__(self):
        self._update()
        return self._median_func()
