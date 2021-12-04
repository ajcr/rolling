from collections import Counter, deque
from itertools import islice

from .base import RollingObject


DEF_BASE = 719
DEF_MOD = 2 ** 61 - 1


def polynomial_hash_sequence(seq, base=DEF_BASE, mod=DEF_MOD):
    """
    Compute the polynomial hash of a sequence.

    """
    return sum(hash(c) * pow(base, k, mod) for k, c in enumerate(reversed(seq))) % mod


class PolynomialHash(RollingObject):
    """
    Rolling polynomial hash.

    Computes a hash of a window of size k as:

        hash(w_0) * base ** (k - 1)
      + hash(w_1) * base ** (k - 2)
      + ...
      + hash(w_(k-2)) * base
      + hash(w_(k-1))
      % mod

    where `base` and `mod` are constant integers.

    To minimise collisions, it is recommended that you
    adjust these values to meet your specific use case.

    See: wikipedia.org/wiki/Rolling_hash#Polynomial_rolling_hash

    Parameters
    ----------

    iterable : iterable of hashable objects
    window_size : integer, the size of the rolling
        window moving over the iterable
    window_type : str, "fixed" or "variable"
    base : integer, polynomial base
    mod : integer, all hashes are modulus this value

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k)

    where k is the size of the rolling window

    Examples
    --------

    >>> import rolling
    >>> r_hash = rolling.PolynomialHash("abcxyabc", window_size=3,
    ...                                 base=31, mod=9967)
    >>> list(r_hash)
    [4984, 900, 5072, 771, 8757, 4984]
    """

    def __init__(
        self, iterable, window_size, window_type="fixed", base=DEF_BASE, mod=DEF_MOD
    ):
        self._hash = 0
        self._base = base
        self._mod = mod
        super().__init__(iterable, window_size, window_type)

    def _init_fixed(self, *args, **kwargs):
        self._buffer = deque([0])
        for val in islice(self._iterator, self.window_size - 1):
            self._add_new(val)

    def _init_variable(self, *args, **kwargs):
        self._buffer = deque()

    def _add_new(self, new):
        self._hash *= self._base
        self._hash += hash(new)
        self._hash %= self._mod
        self._buffer.append(new)

    def _remove_old(self):
        old = self._buffer.popleft()
        self._hash -= hash(old) * pow(self._base, self._obs, self._mod)
        self._hash %= self._mod

    def _update_window(self, new):
        self._remove_old()
        self._add_new(new)

    @property
    def current_value(self):
        return self._hash

    @property
    def _obs(self):
        return len(self._buffer)
