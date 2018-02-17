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

    @property
    def current_value(self):
        return self._sum / self._obs


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

    def _init_fixed(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        if window_size <= 1:
            raise ValueError('Window size must be greater than 1')

        self._buffer = deque(maxlen=window_size)
        self._mean = 0.0 # mean of values
        self._m2 = 0.0  # sum of squared values less the mean

        head = islice(self._iterator, window_size - 1)
        for value in head:
            self._buffer.append(value)
            delta = value - self._mean
            self._mean += delta / self._obs
            self._m2 += delta * (value - self._mean)

        # insert mean at the start of the buffer so that the
        # the first call to update returns the correct value
        # note: self._i is now (window_size - 1)
        self._buffer.appendleft(self._mean)

    def _init_variable(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        if window_size <= 1:
            raise ValueError('Window size must be greater than 1')

        self._buffer = deque(maxlen=window_size)
        self._mean = 0.0 # mean of values
        self._m2 = 0.0  # sum of squared values less the mean

    def _add_new(self):
        new = next(self._iterator)
        self._buffer.append(new)

        delta = new - self._mean
        self._mean += delta / self._obs
        self._m2 += delta * (new - self._mean)

    def _remove_old(self):
        old = self._buffer.popleft()

        delta = old - self._mean
        self._mean -= delta / self._obs
        self._m2 -= delta * (old - self._mean)

    def _update(self):
        new = next(self._iterator)
        old = self._buffer[0]
        self._buffer.append(new)

        delta = new - old
        delta_old = old - self._mean
        self._mean += delta / self._obs
        delta_new = new - self._mean
        self._m2 += delta * (delta_old + delta_new)

    @property
    def current_value(self):
        if self._obs == 1:
            return float('nan')
        else:
            return self._m2 / (self._obs - 1)

    @property
    def _obs(self):
        return len(self._buffer)

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

    @property
    def current_value(self):
        if self._obs == 1:
            return float('nan')
        else:
            return sqrt(self._m2 / (self._obs - 1))



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

    def _init_fixed(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
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

    def _init_variable(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        self._buffer = deque(maxlen=window_size)
        self._skiplist = IndexableSkiplist(window_size)

    def _update(self):
        new = next(self._iterator)
        old = self._buffer[0]
        self._skiplist.remove(old)
        self._skiplist.insert(new)
        self._buffer.append(new)

    def _add_new(self):
        new = next(self._iterator)
        self._skiplist.insert(new)
        self._buffer.append(new)

    def _remove_old(self):
        old = self._buffer[0]
        self._skiplist.remove(old)
        self._buffer.popleft()

    @property
    def current_value(self):
        if self._obs % 2 == 1:
            return self._skiplist[self._obs // 2]
        else:
            i = self._obs // 2
            return (self._skiplist[i] + self._skiplist[i-1]) / 2

    @property
    def _obs(self):
        return len(self._buffer)
