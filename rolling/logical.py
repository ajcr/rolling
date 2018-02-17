from collections import deque
from itertools import islice

from .base import RollingObject


class RollingAll(RollingObject):
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

    >>> seq = (8, 0, 1, 3, 6, 5)
    >>> r_all = RollingAll(seq, 3)
    >>> next(r_all)
    False
    >>> next(r_all)
    False
    >>> r_all = RollingSum(seq, 4)
    >>> list(r_all)
    [False, False, True]

    Notes
    -----

    This object can also be instantiated using the
    `rolling()` function by passing 'All':

    >>> from rolling import rolling
    >>> r_all = rolling(seq, window_size=3, func='All')

    """
    _func_name = 'All'

    def _init_fixed(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        head = islice(self._iterator, window_size - 1)
        self._i = 0
        self._last_false = -1
        for val in head:
            self._i += 1
            if not val:
                self._last_false = self._i
        self._obs = window_size
        # all([]) is True
        self._all = True

    def _init_variable(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        self._i = 0
        self._obs = 0
        self._last_false = -1
        self._all = True # all([]) is True

    def _add_new(self):
        val = next(self._iterator)
        self._i += 1
        self._obs += 1
        if not val:
            self._last_false = self._i - 1
        self._all = self._i - self._obs > self._last_false

    def _update(self):
        val = next(self._iterator)
        self._i += 1
        if not val:
            self._last_false = self._i
        #self._all = self._i - self._last_false > self._obs
        self._all = self._i - self._obs >= self._last_false

    def _remove_old(self):
        self._obs -= 1
        self._all = self._i - self._obs > self._last_false

    @property
    def current_value(self):
        #return self._i - self._last_false > self._obs
        #return self._obs + self._last_false < self._i
        return self._all


class RollingAny(RollingObject):
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

    >>> seq = (1, 0, 0, 0, 6, 5)
    >>> r_any = RollingAny(seq, 3)
    >>> next(r_any)
    True
    >>> next(r_any)
    False
    >>> r_any = RollingAny(seq, 4)
    >>> list(r_any)
    [True, True, True]

    Notes
    -----

    This object can also be instantiated using the
    `rolling()` function by passing 'Any':

    >>> from rolling import rolling
    >>> r_any = rolling(seq, window_size=3, func='Any')

    """
    _func_name = 'Any'

    def _init_fixed(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        head = islice(self._iterator, window_size - 1)
        self._i = -1
        self._last_true = -1
        self._obs = window_size
        for val in head:
            self._i += 1
            if val:
                self._last_true = self._i

    def _init_variable(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        self._i = -1
        self._last_true = -1

    def _add_new(self):
        self._i += 1
        val = next(self._iterator)
        if val:
            self._last_true = self._i

    _update = _add_new

    def _remove_old(self):
        # no operation required
        pass

    @property
    def current_value(self):
        return self._i - self._last_true < self._obs


class RollingCount(RollingObject):
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

    >>> seq = (1, 0, 0, 0, 6, 5)
    >>> r_count = RollingCount(seq, 3)
    >>> next(r_count)
    1
    >>> next(r_count)
    0
    >>> r_count = RollingCount(seq, 4)
    >>> list(r_count)
    [1, 1, 2]

    Notes
    -----

    This object can also be instantiated using the
    `rolling()` function by passing 'Count':

    >>> from rolling import rolling
    >>> r_count = rolling(seq, window_size=3, func='Count')

    """
    _func_name = 'Count'

    def _init_fixed(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(map(bool, head), maxlen=window_size)
        self._buffer.appendleft(False)
        self._count = sum(self._buffer)

    def _init_variable(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
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
