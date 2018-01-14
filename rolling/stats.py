from collections import deque
from itertools import islice
from math import sqrt

from .base import RollingObject
from .arithmetic import RollingSum
from .structures.skiplist import IndexableSkiplist


class RollingMean(RollingSum):
    """Compute the mean value of a rolling window.

    The cost of updating the mean is O(1), and the
    O(k) space is required.
    """
    _func_name = 'Mean'

    def __next__(self):
        self._update()
        return self._sum / self.window_size


class RollingVar(RollingObject):
    """Compute the variance of a rolling window.

    Uses Welford's algorithm to update the sample
    variance (k-1 degrees of freedom) and mean each
    time the window is moved forward.

    The cost of updating the value is O(1), and the
    O(k) space is required.

    See https://en.wikipedia.org/w/index.php?title=Algorithms_for_calculating_variance&oldid=617145179
    """
    _func_name = 'Var'

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)

        if window_size <= 1:
            raise ValueError('Window size must be greater than 1')

        self._buffer = deque([], maxlen=window_size)

        self._i = 0 # degrees of freedom
        self._mean = 0.0 # mean
        self._m2 = 0.0  # sum of squared values less the mean

        for i in range(1, window_size):
            self._i += 1
            self._add_new()

        # insert mean at the start of the buffer so that the
        # the first call to update returns the correct value
        # note: self._i is now (window_size - 1)
        self._buffer.appendleft(self._mean)

    def _add_new(self):
        new = next(self._iterator)

        delta = new - self._mean
        self._mean += delta / self._i
        self._m2 += delta * (new - self._mean)

        self._buffer.append(new)

    # implemented for completeness - not used and untested
    def _remove_old(self):
        old = self._buffer.popleft()

        delta = old - self._mean
        self._mean -= delta / (self._i - 1)
        self._m2 -= delta * (old - self._mean)

    def _update(self):
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
    """Compute the standard deviation of a rolling window.

    Uses Welford's algorithm to update the sample
    standard deviation (k-1 degrees of freedom) and mean
    each time the window is moved forward.

    The cost of updating the value is O(1), and
    O(k) space is required.

    See https://en.wikipedia.org/w/index.php?title=Algorithms_for_calculating_variance&oldid=617145179
    """
    _func_name = 'Std'

    def __next__(self):
        self._update()
        return sqrt(self._m2 / self._i)


class RollingMedian(RollingObject):
    """Iterator object that computes the median
    of a rolling window over a Python iterable.

    The cost of updating median in the rolling
    window is O(log k) and the memory used is O(k)
    where k is the size of the window.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Notes
    -----

    This object can also be instantiated using the
    `rolling()` function by passing 'Median':

    >>> from rolling import rolling
    >>> r_median = rolling(seq, window_size=3, func='Median')

    To track the median, an indexable skiplist is
    used. This approach was taken from work done
    by Raymond Hettinger (see for example [1]).

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
