from collections import deque
from itertools import islice
from math import sqrt

from rolling.base import RollingObject


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
