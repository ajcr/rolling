from collections import deque, namedtuple

from .base import RollingObject

# TODO: reduce code duplication between RollingMin and RollingMax

pair = namedtuple('pair', ['value', 'death'])

class RollingMin(RollingObject):
    """Compute the minimum value in the rolling window.

    Uses the ascending minima algorithm described in [1]
    to compute each value in O(1) time and O(k) space.

    [1] http://www.richardhartersworld.com/cri/2001/slidingmin.html
    """
    _func_name = 'Min'

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)
        self._iterator = enumerate(self._iterator)

        self._buffer = deque()

        for _ in range(window_size - 1):
            self._update()

    def _update(self):
        buffer = self._buffer
        i, value = next(self._iterator)
        new_pair = pair(value, i + self.window_size)

        # remove everything greater to or equal to the new value
        while buffer and buffer[-1].value >= value:
            buffer.pop()

        buffer.append(new_pair)

        # remove minimal values that died on or before this iteration
        while buffer[0].death <= i:
            buffer.popleft()

    def __next__(self):
        self._update()
        return self._buffer[0].value


class RollingMax(RollingObject):
    """Compute the maximum value in the rolling window.

    Uses the descending maxima algorithm described in [1]
    to compute each value in O(1) time and O(k) space.

    [1] http://www.richardhartersworld.com/cri/2001/slidingmin.html
    """
    _func_name = 'Max'

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)
        self._iterator = enumerate(self._iterator)

        self._buffer = deque()

        for _ in range(window_size - 1):
            self._update()

    def _update(self):
        buffer = self._buffer
        i, value = next(self._iterator)
        new_pair = pair(value, i + self.window_size)

        # remove everything greater to or equal to the new value
        while buffer and buffer[-1].value <= value:
            buffer.pop()

        buffer.append(new_pair)

        # remove minimal values that died on or before this iteration
        while buffer[0].death <= i:
            buffer.popleft()

    def __next__(self):
        self._update()
        return self._buffer[0].value
