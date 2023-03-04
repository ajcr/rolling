from collections import Counter, deque
from itertools import islice
from math import fsum, log2, log10, log

from rolling.base import RollingObject


def _get_log_func(base):
    if base == 2:
        return log2
    if base == 10:
        return log10
    if base == "e":
        return log
    return lambda x: log(x, base)


def entropy(seq, base=2, reference_distribution=None):
    N = len(seq)
    counts = Counter(seq)
    _log = _get_log_func(base)
    if reference_distribution is None:
        return -fsum((c / N) * _log(c / N) for c in counts.values())
    return fsum(
        (c / N) * _log(c / N / reference_distribution[k])
        for k, c in counts.items()
    )


class Entropy(RollingObject):
    """
    Entropy of a rolling window.

    The count of each value, x, in the window is interpreted as
    the probability, p(x), of the value occuring. The entropy of
    the window is then understood as the average number of units
    of information per value in the window.

    If no reference distribution is given, the window value is the
    Shannon Entropy. If a reference distribution is given, the
    value is the relative entropy (Kullback-Leibler Divergence).

    Note: window_type='variable' is not supported.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable
    base : logarithm base to use (default=2)
    reference_distribution : Mapping[Hashable, float] : actual
        probabilities for values in window, allowing relative
        entropy to be computed (KL-divergence).

    Complexity
    ----------

    Update time:  O(1) (for fixed-length windows)
    Memory usage: O(k)

    where k is the size of the rolling window

    Examples
    --------

    >>> import rolling
    >>> seq = 'aaaaaaaaaxaxxvazsdzsdqrmke'
    >>> r_entropy = rolling.Entropy(seq, 10)
    >>> list(r_entropy)
    [0.4689955935892812,
     0.4689955935892812,
     0.7219280948873623,
     0.8812908992306927,
     1.295461844238322,
     1.295461844238322,
     1.6854752972273344,
     2.046439344671015,
     ...]

    """
    def __init__(self, iterable, window_size, base=2, reference_distribution=None):
        if reference_distribution is not None and sum(reference_distribution.values()) != 1:
            raise ValueError("reference_distribution probabilities must sum to 1")
        self.reference_distribution = reference_distribution
        self._log = _get_log_func(base)
        super().__init__(iterable, window_size)

    def _init_fixed(self, iterable, window_size, **kwargs):
        self._entropy = 0.0
        self._summands = {}

        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)

        counts = Counter(self._buffer)

        for value, count in counts.items():
            x = self._compute_summand(value, count)
            self._summands[value] = (count, x)
            self._entropy -= x

        # insert a dummy value that is removed when next() is called
        self._buffer.appendleft(object)
        self._summands[object] = (1, 0)

    def _init_variable(self, iterable, window_size, **kwargs):
        raise NotImplementedError("Entropy not implemented for variable windows")

    def _update_window(self, new):
        old = self._buffer[0]
        self._buffer.append(new)

        # if there's nothing to update just return
        if old == new:
            return

        # remove old summand's contribution to entropy
        count, summand = self._summands[old]
        self._entropy += summand

        if count == 1:
            del self._summands[old]
        else:
            x = self._compute_summand(old, count-1)
            self._summands[old] = (count-1, x)
            self._entropy -= x

        # update new summand's contribution to entropy
        count, summand = self._summands.get(new, (0, 0))
        x = self._compute_summand(new, count+1)
        self._summands[new] = (count+1, x)
        self._entropy += summand - x

    def _compute_summand(self, value, count):
        p = count / self.window_size
        if self.reference_distribution is None:
            return p * self._log(p)
        return p * self._log(p / self.reference_distribution[value])

    @property
    def current_value(self):
        return abs(self._entropy)

    @property
    def _obs(self):
        return len(self._buffer)

    # Required, but unused as variable windows not supported
    def _add_new(self, new):
        pass

    def _remove_old(self):
        pass
