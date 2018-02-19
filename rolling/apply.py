from collections import deque
from itertools import islice

from .base import RollingObject


class Apply(RollingObject):
    """Apply a specific function to a rolling window"""

    def _init_fixed(self, iterable, window_size, operation=sum, **kwargs):
        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)
        self._operation = operation

    def _init_variable(self, iterable, window_size, operation=sum, **kwargs):
        self._buffer = deque(maxlen=window_size)
        self._operation = operation

    @property
    def current_value(self):
        return self._operation(self._buffer)

    def _add_new(self):
        self._buffer.append(next(self._iterator))

    def _remove_old(self):
        self._buffer.popleft()

    def _update(self):
        self._buffer.append(next(self._iterator))

    @property
    def _obs(self):
        return len(self._buffer)

    def __repr__(self):
        return "Rolling(operation='{}', window_size={}, window_type='{}')".format(
                    self._operation.__name__, self.window_size, self.window_type)
