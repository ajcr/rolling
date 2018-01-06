from collections import deque

from .base import RollingObject
from .arithmetic import RollingSum


class RollingMean(RollingSum):
    """Compute the mean value of a rolling window.

    The cost of updating the mean is O(1), and the
    O(k) space is required.
    """
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

