from collections import Counter, deque
from itertools import islice
from math import fsum, log2

from .base import RollingObject


def _test_entropy(sequence):
    """Compute the Shannon entropy of a sequence
    in a standard way (used for testing).
    """
    N = len(sequence)
    counts = Counter(sequence)
    return -fsum((c / N) * log2(c / N) for c in counts.values())


class Entropy(RollingObject):
    """Iterator object that computes the Shannon
    entropy of a rolling window over a Python iterable.

    Note: only window_type='fixed' is supported.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Complexity
    ----------

    Update time:  O(1) when the overall size of
        window does not change, O(k) otherwise
    Memory usage: O(k)

    where k is the size of the rolling window

    Examples
    --------

    >>> import rolling
    >>> seq = 'aabbbmbbbbccaaaabcba'
    >>> r_entropy = rolling.Entropy(seq, 15)
    >>> list(r_entropy)
    [1.6894822670191827,
     1.6894822670191827,
     1.640223928941852,
     1.7464657985040721,
     1.7464657985040721,
     1.7819370635467044]

    """
    def _init_fixed(self, iterable, window_size, **kwargs):
        self._entropy = 0.0
        self._summands = {}

        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)

        counts = Counter(self._buffer)

        for value, count in counts.items():
            x = (count / window_size) * log2(count / window_size)
            self._summands[value] = (count, x)
            self._entropy -= x

        # insert a dummy value that is removed when next() is called
        self._buffer.appendleft('dummy_value')
        x = (1 / window_size) * log2(1 / window_size)
        self._summands['dummy_value'] = (1, x)
        self._entropy -= x

    def _init_variable(self, iterable, window_size, **kwargs):
        raise NotImplementedError('Entropy not implemented for variable windows')

    def _update_window(self, new):
        old = self._buffer[0]
        self._buffer.append(new)

        # if there's nothing to update, exit
        if old == new:
            return

        # remove old summand's contribution to entropy
        count, summand = self._summands[old]
        self._entropy += summand

        if count == 1:
            del self._summands[old]
        else:
            p_old = (count - 1) / self.window_size
            # readjust entropy
            log_p_old = log2(p_old)
            self._summands[old] = (count - 1, p_old * log_p_old)
            self._entropy -= p_old * log_p_old

        # update new summand's contribution to entropy
        if new in self._summands:
            count, summand = self._summands[new]
            p_new = (count + 1) / self.window_size
            log_p_new = log2(p_new)
            self._summands[new] = (count + 1, p_new * log_p_new)
            self._entropy += summand - (p_new * log_p_new)

        else:
            p_new = 1 / self.window_size
            log_p_new = log2(p_new)
            self._summands[new] = (1, p_new * log_p_new)
            self._entropy -= (p_new * log_p_new)

    def _add_new(self, new):
        pass

    def _remove_old(self):
        pass

    @property
    def current_value(self):
        return self._entropy

    @property
    def _obs(self):
        return len(self._buffer)
