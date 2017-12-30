from .base import RollingObject


class RollingAll(RollingObject):
    """Compute whether all values in the window are true.

    The cost of updating the window is constant, as is the
    space used by the algorithm.
    """
    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)
        self._consecutive_true = 0
        for _ in range(window_size - 1):
            self._update()

    def _update(self):
        if next(self._iterator):
            self._consecutive_true += 1
        else:
            self._consecutive_true = 0

    def __next__(self):
        self._update()
        return self._consecutive_true >= self.window_size


class RollingAny(RollingObject):
    """Compute whether any value in the window is true.

    The cost of updating the window is constant, as is the
    space used by the algorithm.
    """

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)
        self._last_true = 0
        for _ in range(window_size - 1):
            self._update()

    def _update(self):
        if next(self._iterator):
            self._last_true = self.window_size
        else:
            self._last_true -= 1

    def __next__(self):
        self._update()
        return self._last_true > 0
