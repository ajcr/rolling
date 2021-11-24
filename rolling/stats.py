from collections import deque
from itertools import islice
from math import sqrt

from .base import RollingObject
from .arithmetic import Sum
from .structures.skiplist import IndexableSkiplist
from .structures.bicounter import BiCounter


class Mean(Sum):
    """
    Iterator object that computes the mean of
    a rolling window over a Python iterable.

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
    """
    Iterator object that computes the variance
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
            raise ValueError("window_size must be greater than ddof")

        self.ddof = ddof
        self._buffer = deque(maxlen=window_size)
        self._mean = 0.0  # mean of values
        self._sslm = 0.0  # sum of squared values less the mean

        for new in islice(self._iterator, window_size - 1):
            self._add_new(new)

        # insert mean at the start of the buffer so that the
        # the first call to update returns the correct value
        self._buffer.appendleft(self._mean)

    def _init_variable(self, iterable, window_size, ddof=1, **kwargs):
        if window_size <= ddof:
            raise ValueError("window_size must be greater than ddof")

        self.ddof = ddof
        self._buffer = deque(maxlen=window_size)
        self._mean = 0.0  # mean of values
        self._sslm = 0.0  # sum of squared values less the mean

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
            return float("nan")
        elif self._sslm < 0:
            self._sslm = 0.0
            return 0.0
        else:
            return self._sslm / (self._obs - self.ddof)

    @property
    def _obs(self):
        return len(self._buffer)


class Std(Var):
    """
    Iterator object that computes the standard deviation
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
        variance = super().current_value
        return sqrt(variance)


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
            return self._bicounter.most_common_items, self._bicounter.largest_count
        else:
            return self._bicounter.most_common_items

    @property
    def _obs(self):
        return len(self._buffer)


class Skew(RollingObject):
    """
    Iterator object that computes the skewness
    of a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable (must be
        greater than 2)

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k)

    where k is the size of the rolling window

    Notes
    -----

    This implementation of rolling skewness is based
    on the pandas code here:

    https://github.com/pandas-dev/pandas/blob/master/pandas/_libs/window.pyx

    """

    def _init_fixed(self, iterable, window_size, **kwargs):
        if window_size <= 2:
            raise ValueError("window_size must be greater than 2")

        self._buffer = deque(maxlen=window_size)
        self._x1 = 0.0
        self._x2 = 0.0
        self._x3 = 0.0

        for new in islice(self._iterator, window_size - 1):
            self._add_new(new)

        # insert zero at the start of the buffer so that the
        # the first call to update returns the correct value
        self._buffer.appendleft(0)

    def _init_variable(self, iterable, window_size, **kwargs):
        if window_size <= 2:
            raise ValueError("window_size must be greater than 2")

        self._buffer = deque(maxlen=window_size)
        self._x1 = 0.0
        self._x2 = 0.0
        self._x3 = 0.0

    def _add_new(self, new):
        self._buffer.append(new)

        self._x1 += new
        self._x2 += new * new
        self._x3 += new * new * new

    def _remove_old(self):
        old = self._buffer.popleft()

        self._x1 -= old
        self._x2 -= old * old
        self._x3 -= old * old * old

    def _update_window(self, new):
        old = self._buffer[0]
        self._buffer.append(new)

        self._x1 += new - old
        self._x2 += new * new - old * old
        self._x3 += new * new * new - old * old * old

    @property
    def current_value(self):
        N = self._obs

        if N < 3:
            return float("nan")

        # compute moments
        A = self._x1 / N
        B = self._x2 / N - A * A
        C = self._x3 / N - A * A * A - 3 * A * B

        if B <= 1e-14:
            return float("nan")

        R = sqrt(B)

        return (sqrt(N * (N - 1)) * C) / ((N - 2) * R * R * R)

    @property
    def _obs(self):
        return len(self._buffer)


class Kurtosis(RollingObject):
    """
    Iterator object that computes the kurtosis
    of a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable (must be
        greater than 3)

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k)

    where k is the size of the rolling window

    Notes
    -----

    This implementation of rolling kurtosis is based
    on the pandas code here:

    https://github.com/pandas-dev/pandas/blob/master/pandas/_libs/window.pyx

    """

    def _init_fixed(self, iterable, window_size, **kwargs):
        if window_size <= 3:
            raise ValueError("window_size must be greater than 3")

        self._buffer = deque(maxlen=window_size)
        self._x1 = 0.0
        self._x2 = 0.0
        self._x3 = 0.0
        self._x4 = 0.0

        for new in islice(self._iterator, window_size - 1):
            self._add_new(new)

        # insert zero at the start of the buffer so that the
        # the first call to update returns the correct value
        self._buffer.appendleft(0)

    def _init_variable(self, iterable, window_size, **kwargs):
        if window_size <= 3:
            raise ValueError("window_size must be greater than 3")

        self._buffer = deque(maxlen=window_size)
        self._x1 = 0.0
        self._x2 = 0.0
        self._x3 = 0.0
        self._x4 = 0.0

    def _add_new(self, new):
        self._buffer.append(new)

        self._x1 += new
        self._x2 += new * new
        self._x3 += new ** 3
        self._x4 += new ** 4

    def _remove_old(self):
        old = self._buffer.popleft()

        self._x1 -= old
        self._x2 -= old * old
        self._x3 -= old ** 3
        self._x4 -= old ** 4

    def _update_window(self, new):
        old = self._buffer[0]
        self._buffer.append(new)

        self._x1 += new - old
        self._x2 += new * new - old * old
        self._x3 += new ** 3 - old ** 3
        self._x4 += new ** 4 - old ** 4

    @property
    def current_value(self):
        N = self._obs

        if N <= 3:
            return float("nan")

        # compute moments
        A = self._x1 / N
        R = A * A

        B = self._x2 / N - R
        R *= A

        C = self._x3 / N - R - 3 * A * B
        R *= A

        D = self._x4 / N - R - 6 * B * A * A - 4 * C * A

        if B <= 1e-14:
            return float("nan")

        K = (N * N - 1) * D / (B * B) - 3 * ((N - 1) ** 2)
        return K / ((N - 2) * (N - 3))

    @property
    def _obs(self):
        return len(self._buffer)
