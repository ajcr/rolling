from collections import defaultdict

from .hash import PolynomialHash, polynomial_hash_sequence, DEF_BASE, DEF_MOD


class Match(PolynomialHash):
    """
    Rolling sequence matching.

    Return true if the window is equal to at least one of
    a set of target matches, and return false otherwise.

    Works by computing the hash of the rolling window and
    comparing it against the hashes of the target matches.
    The sequences are only compared is the window hash
    matches one of the target hashes.

    Note that the update complexity is worst case linear when
    the window matches a target sequence. If there is no match,
    the update time is typically O(1) (if few hash collisions).

    Parameters
    ----------

    iterable : sequence of sequences (of same length)
    match : sequence of sequence objects to match
        against the rolling window
    base : integer, polynomial base
    mod : integer, all hashes are modulus this value

    See rolling.PolynomialHash() for further context around
    the base and mod values.

    Complexity
    ----------

    Update time:  O(1) if no match, O(k) if a possible match
    Memory usage: O(k)

    where k is the size of the rolling window

    Examples
    --------

    >>> import rolling
    >>> r_match = rolling.Match("loremipsum", match=["sum", "rem"])
    >>> list(r_match)
    [False, False, True, False, False, False, False, True]
    """

    def __init__(self, iterable, match, base=DEF_BASE, mod=DEF_MOD):

        self.match = match

        # For each target match sequence, compute its polynomial hash
        # and keep a dictionary of {hash: List[sequence]}.
        #
        # Note that the values need to be a list and not a set since
        # the sequences may not be hashable.
        self._hash_match = defaultdict(list)

        for sequence in match:
            if len(sequence) != len(match[0]):
                raise ValueError("All match sequences must be the same length")
            hash_ = polynomial_hash_sequence(sequence)
            self._hash_match[hash_].append(sequence)

        super().__init__(
            iterable, window_size=len(match[0]), window_type="fixed", base=base, mod=mod
        )

    @property
    def current_value(self):
        if self._hash not in self._hash_match:
            return False
        return any(is_equal(self._buffer, seq) for seq in self._hash_match[self._hash])


def is_equal(seq_1, seq_2):
    return all(s1 == s2 for s1, s2 in zip(seq_1, seq_2))
