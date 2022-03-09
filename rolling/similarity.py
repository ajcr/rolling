from collections import Counter, deque
from itertools import islice

from .base import RollingObject


def jaccard_index(a, b):
    a_set = set(a)
    b_set = set(b)
    return len(a_set & b_set) / len(a_set | b_set)



class JaccardIndex(RollingObject):
    """
    Rolling Jaccard index.

    Computes the Jaccard index similarity coefficient measuring
    the similarity between the window and a target set (between
    0 and 1).

    The value is the size of the intersection of the window
    and the target set, divided by the size of the union
    of the window and target set.

    Parameters
    ----------

    iterable : iterable of hashable objects
    window_size : integer, the size of the rolling
        window moving over the iterable
    window_type : str, "fixed" or "variable"
    target_set : sequence of hashable objects

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k + |target_set|)

    where k is the size of the rolling window

    Examples
    --------

    >>> import rolling
    >>> primes = {2, 3, 5, 7, 11}
    >>> seq = range(1, 10)
    >>> r_jacc = rolling.JaccardIndex(seq, window_size=4, target_set=primes)
    >>> list(r_jacc)
    [0.2857142857142857,
     0.5,
     0.2857142857142857,
     0.2857142857142857,
     0.2857142857142857,
     0.125]

    """
    def __init__(self, iterable, window_size, target_set, window_type="fixed"):
        self._target_set = frozenset(target_set)
        if not self._target_set:
            raise ValueError("target_set cannot be empty")
        self._buffer = deque()
        self._intersection = Counter()
        self._union = Counter(self._target_set)
        super().__init__(iterable, window_size, window_type)

    def _init_fixed(self, *args, **kwargs):
        self._buffer.append(None)
        for val in islice(self._iterator, self.window_size - 1):
            self._add_new(val)

    def _init_variable(self, *args, **kwargs):
        pass

    def _add_new(self, new):
        self._buffer.append(new)
        self._union[new] += 1
        if new in self._target_set:
           self._intersection[new] += 1 

    def _remove_old(self):
        old = self._buffer.popleft()
        for mapping in (self._intersection, self._union):
            if old in mapping:
                if mapping[old] <= 1:
                    del mapping[old]
                else:
                    mapping[old] -= 1

    def _update_window(self, new):
        self._remove_old()
        self._add_new(new)

    @property
    def current_value(self):
        return len(self._intersection) / len(self._union)

    @property
    def _obs(self):
        return len(self._buffer)
