from collections import Counter, deque
from itertools import islice

from rolling.base import RollingObject


class Nunique(RollingObject):
    """
    Iterator object that counts the number of
    unique values in a rolling window.

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
    >>> word = 'mississippi'
    >>> r_nunique = rolling.Nunique(word, 3)
    >>> next(r_nunique)
    3
    >>> next(r_nunique)
    2
    >>> r_nunique = rolling.Nunique(word, 4)
    >>> list(r_nunique)
    [3, 2, 2, 2, 2, 3, 3]

    """

    def _init_fixed(self):
        head = islice(self._iterator, self.window_size - 1)
        self._buffer = deque(head)
        # append a dummy value that is removed when next() is called
        self._buffer.appendleft("dummy_value")
        self._counter = Counter(self._buffer)

    def _init_variable(self):
        self._buffer = deque()
        self._counter = Counter()

    _init_indexed = _init_variable

    def _update_window(self, new):
        # remove oldest value before appending new to buffer
        self._remove_old()
        self._counter[new] += 1
        self._buffer.append(new)

    def _add_new(self, new):
        self._counter[new] += 1
        self._buffer.append(new)

    def _remove_old(self):
        old = self._buffer.popleft()
        self._counter -= Counter([old])

    @property
    def current_value(self):
        return len(self._counter)

    @property
    def _obs(self):
        return len(self._buffer)
