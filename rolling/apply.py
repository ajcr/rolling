from collections import deque
from itertools import islice

from .base import RollingObject


class RollingApply(RollingObject):
    """Apply a callable to a window"""
    def _init_fixed(self, iterable, window_size, func, **kwargs):
        super().__init__(iterable, window_size)
        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)
        self._func = func

    def _init_variable(self, iterable, window_size, func, **kwargs):
        super().__init__(iterable, window_size)
        self._buffer = deque(maxlen=window_size)
        self._func = func
        self._filled = False

    @property
    def _buffer_len(self):
        return len(self._buffer)

    @property
    def current_value(self):
        return self._func(self._buffer)

    def _add_new(self):
        self._buffer.append(next(self._iterator))

    def _remove_old(self):
        self._buffer.popleft()

    def _update(self):
        self._buffer.append(next(self._iterator))

    def _next_fixed(self):
        self._update()
        return self.current_value

    def _next_variable(self):
        # while the window size is not reached, add new values
        if not self._filled and self._buffer_len < self.window_size:
            self._add_new()
            if self._buffer_len == self.window_size:
                self._filled = True
            return self.current_value
        # once the window size is reached, update until the iterator finishes
        try:
            self._add_new()
            return self.current_value
        except StopIteration:
            # once iterator finishes, remove the oldest values one by one
            if self._buffer_len == 1:
                raise
            else:
                self._remove_old()
                return self.current_value
