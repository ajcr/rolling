from collections import deque
from itertools import islice
from math import sqrt

from .base import RollingObject
from .arithmetic import Sum
from .structures.skiplist import IndexableSkiplist


class Mean(Sum):
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
    @property
    def current_value(self):
        return self._sum / self._obs


class Var(RollingObject):
    """Iterator object that computes the variance
    of a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable
    ddof : int, default 1, the divisor used in calculation
        is (N - ddof) where N is the number of observations

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k)

    where k is the size of the rolling window

    Notes
    -----

    Welford's algorithm is used to compute the variance.

    Note that ddof must be less than window_size, otherwise
    a value error is raised during initialisation.

    Otherwise, if (N - ddof) is less than 0 (for variable-size
    windows), the variance is computed as NaN.
    """
    def _init_fixed(self, iterable, window_size, ddof=1, **kwargs):
        if window_size <= ddof:
            raise ValueError('window_size must be greater than ddof')

        self.ddof = ddof
        self._buffer = deque(maxlen=window_size)
        self._mean = 0.0 # mean of values
        self._sslm = 0.0 # sum of squared values less the mean

        for new in islice(self._iterator, window_size-1):
            self._add_new(new)

        # insert mean at the start of the buffer so that the
        # the first call to update returns the correct value
        self._buffer.appendleft(self._mean)

    def _init_variable(self, iterable, window_size, ddof=1, **kwargs):
        if window_size <= ddof:
            raise ValueError('window_size must be greater than ddof')

        self.ddof = ddof
        self._buffer = deque(maxlen=window_size)
        self._mean = 0.0 # mean of values
        self._sslm = 0.0 # sum of squared values less the mean

    def _add_new(self, new):
        self._buffer.append(new)

        delta = new - self._mean
        self._mean += delta / self._obs
        self._sslm += delta * (new - self._mean)

    def _remove_old(self):
        old = self._buffer.popleft()

        delta = old - self._mean
        self._mean -= delta / self._obs
        self._sslm -= delta * (old - self._mean)

    def _update_window(self, new):
        old = self._buffer[0]
        self._buffer.append(new)

        delta = new - old
        delta_old = old - self._mean
        self._mean += delta / self._obs
        delta_new = new - self._mean
        self._sslm += delta * (delta_old + delta_new)

    @property
    def current_value(self):
        if self._obs <= self.ddof:
            return float('nan')
        else:
            return self._sslm / (self._obs - self.ddof)

    @property
    def _obs(self):
        return len(self._buffer)


class Std(Var):
    """Iterator object that computes the standard deviation
    of a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable
    ddof : int, default 1, the divisor used in calculation
        is (N - ddof) where N is the number of observations

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k)

    where k is the size of the rolling window

    Notes
    -----

    Welford's algorithm is used to compute the variance,
    of which the standard deviation is the square root.

    Note that ddof must be less than window_size, otherwise
    a value error is raised during initialisation.

    Otherwise, if N-ddof is less than 0 (for variable-size
    windows), the variance is computed as NaN.
    """
    @property
    def current_value(self):
        if self._obs <= self.ddof:
            return float('nan')
        else:
            return sqrt(self._sslm / (self._obs - self.ddof))


class Median(RollingObject):
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
    def _init_fixed(self, iterable, window_size, **kwargs):
        self._buffer = deque(maxlen=window_size)
        self._skiplist = IndexableSkiplist(window_size)

        # update buffer and skiplist with initial values
        for new in islice(self._iterator, window_size-1):
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
            return (self._skiplist[i] + self._skiplist[i-1]) / 2

    @property
    def _obs(self):
        return len(self._buffer)
