from collections import Counter, deque
from itertools import islice

from rolling.base import RollingObject


class Product(RollingObject):
    """
    Iterator object that computes the product of a
    rolling window over a Python iterable.

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
    >>> seq = (8, 1, 1, 3, 6, 5)
    >>> r_prod = rolling.Product(seq, 3)
    >>> next(r_prod)
    8
    >>> next(r_prod)
    3
    >>> r_prod = rolling.Product(seq, 4)
    >>> list(r_prod)
    [24, 18, 90]

    """

    def _init_fixed(self, iterable, window_size, **kwargs):
        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)
        self._zero_count = 0

        prod = 1

        for value in self._buffer:
            if value:
                prod *= value
            else:
                self._zero_count += 1

        self._buffer.appendleft(1)
        self._product = prod

    def _init_variable(self, iterable, window_size, **kwargs):
        self._buffer = deque(maxlen=window_size)
        self._zero_count = 0
        self._product = 1

    def _update_window(self, new):
        old = self._buffer.popleft()
        self._buffer.append(new)

        if old:
            self._product /= old
        else:
            self._zero_count -= 1

        if new:
            self._product *= new
        else:
            self._zero_count += 1

    def _add_new(self, new):
        self._buffer.append(new)

        if new:
            self._product *= new
        else:
            self._zero_count += 1

    def _remove_old(self):
        old = self._buffer.popleft()

        if old:
            self._product /= old
        else:
            self._zero_count -= 1

    @property
    def current_value(self):
        if self._zero_count:
            return 0
        else:
            return self._product

    @property
    def _obs(self):
        return len(self._buffer)
