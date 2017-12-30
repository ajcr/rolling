from collections import Counter, deque
from itertools import islice

from .base import RollingObject


class RollingApply(RollingObject):
    """Apply any callable to a rolling window.


    """
    def __init__(self, iterable, window_size, func):
        super().__init__(iterable, window_size)

        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)
        self._func = func

    def _update(self):
        self._buffer.append(next(self._iterator))

    def __next__(self):
        self._update()
        return self._func(self._buffer)
