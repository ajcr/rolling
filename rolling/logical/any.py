from collections import deque
from itertools import islice

from rolling.base import RollingObject


class Any(RollingObject):
    """
    Iterator object that computes whether any values
    in a rolling window over a Python iterable
    evaluate to True.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(1)

    Examples
    --------

    >>> import rolling
    >>> seq = (1, 0, 0, 0, 6, 5)
    >>> r_any = rolling.Any(seq, 3)
    >>> next(r_any)
    True
    >>> next(r_any)
    False
    >>> r_any = rolling.Any(seq, 4)
    >>> list(r_any)
    [True, True, True]

    """

    def _init_fixed(self, iterable, window_size, **kwargs):
        self._i = -1
        self._window_obs = 1
        self._last_true = -1
        for new in islice(self._iterator, window_size - 1):
            self._add_new(new)

    def _init_variable(self, iterable, window_size, **kwargs):
        self._i = -1
        self._window_obs = 0
        self._last_true = -1

    def _add_new(self, new):
        self._i += 1
        self._window_obs += 1
        if new:
            self._last_true = self._i

    def _update_window(self, new):
        self._i += 1
        if new:
            self._last_true = self._i

    def _remove_old(self):
        self._window_obs -= 1

    @property
    def _obs(self):
        return self._window_obs

    @property
    def current_value(self):
        return self._i - self._window_obs < self._last_true
