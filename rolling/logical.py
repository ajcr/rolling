from collections import deque
from itertools import islice

from .base import RollingObject


class All(RollingObject):
    """Iterator object that computes whether all
    values in a rolling window over a Python iterable
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
    >>> seq = (8, 0, 1, 3, 6, 5)
    >>> r_all = rolling.All(seq, 3)
    >>> next(r_all)
    False
    >>> next(r_all)
    False
    >>> r_all = rolling.All(seq, 4)
    >>> list(r_all)
    [False, False, True]

    Notes
    -----

    This object can also be instantiated using the
    `rolling()` function by passing 'All':

    >>> from rolling import rolling
    >>> r_all = rolling(seq, window_size=3, operation='All')

    """
    def _init_fixed(self, iterable, window_size, **kwargs):
        head = islice(self._iterator, window_size - 1)
        self._i = 0
        self._last_false = -1
        for val in head:
            self._i += 1
            if not val:
                self._last_false = self._i
        self._obs = window_size

    def _init_variable(self, iterable, window_size, **kwargs):
        self._i = -1
        self._obs = 0
        self._last_false = -window_size - 1

    def _add_new(self):
        val = next(self._iterator)
        self._i += 1
        self._obs += 1
        if not val:
            self._last_false = self._i

    def _update(self):
        val = next(self._iterator)
        self._i += 1
        if not val:
            self._last_false = self._i

    def _remove_old(self):
        self._obs -= 1

    @property
    def current_value(self):
        return self._i - self._obs >= self._last_false


class Any(RollingObject):
    """Iterator object that computes whether any
    values in a rolling window over a Python iterable
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

    Notes
    -----

    This object can also be instantiated using the
    `rolling()` function by passing 'Any':

    >>> from rolling import rolling
    >>> r_any = rolling(seq, window_size=3, operation='Any')

    """
    def _init_fixed(self, iterable, window_size, **kwargs):
        head = islice(self._iterator, window_size - 1)
        self._i = 0
        self._last_true = -1
        for val in head:
            self._i += 1
            if val:
                self._last_true = self._i
        self._obs = window_size

    def _init_variable(self, iterable, window_size, **kwargs):
        self._i = -1
        self._obs = 0
        self._last_true = -window_size - 1

    def _add_new(self):
        val = next(self._iterator)
        self._i += 1
        self._obs += 1
        if val:
            self._last_true = self._i

    def _update(self):
        val = next(self._iterator)
        self._i += 1
        if val:
            self._last_true = self._i

    def _remove_old(self):
        self._obs -= 1

    @property
    def current_value(self):
        return self._i - self._obs < self._last_true


class Count(RollingObject):
    """Iterator object that counts the number of
    values in a rolling window over a Python iterable
    which evaluate to True.

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

    Examples
    --------

    >>> import rolling
    >>> seq = (1, 0, 0, 0, 6, 5)
    >>> r_count = rolling.Count(seq, 3)
    >>> next(r_count)
    1
    >>> next(r_count)
    0
    >>> r_count = rolling.Count(seq, 4)
    >>> list(r_count)
    [1, 1, 2]

    Notes
    -----

    This object can also be instantiated using the
    `rolling()` function by passing 'Count':

    >>> from rolling import rolling
    >>> r_count = rolling(seq, window_size=3, operation='Count')

    """
    def _init_fixed(self, iterable, window_size, **kwargs):
        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(map(bool, head), maxlen=window_size)
        self._buffer.appendleft(False)
        self._count = sum(self._buffer)

    def _init_variable(self, iterable, window_size, **kwargs):
        self._buffer = deque(maxlen=window_size)
        self._count = 0

    def _update(self):
        value = bool(next(self._iterator))
        self._count += value - self._buffer.popleft()
        self._buffer.append(value)

    def _add_new(self):
        value = bool(next(self._iterator))
        self._count += value
        self._buffer.append(value)

    def _remove_old(self):
        self._count -= self._buffer.popleft()

    @property
    def current_value(self):
        return self._count

    @property
    def _obs(self):
        return len(self._buffer)
