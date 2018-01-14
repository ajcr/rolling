from collections import deque, namedtuple
import heapq
from itertools import islice
from operator import ge, le


from .base import RollingObject

pair = namedtuple('pair', ['value', 'death'])


class _RollingMM(RollingObject):
    """Internal class not for instantiation.

    Contains methods common to the Min and Max
    classes below. These classes need only
    implement an _update() method.
    """
    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)
        self._iterator = enumerate(self._iterator)
        self._buffer = deque()
        for _ in range(window_size - 1):
            self._update()

    def __next__(self):
        self._update()
        return self._buffer[0].value


def _make_update_method(op):
    """Helper function to make the _update() method for
    the Min and Max classes, which differ only by op"""
    def _update(self):
        buffer = self._buffer
        i, value = next(self._iterator)
        new_pair = pair(value, i + self.window_size)

        while buffer and op(buffer[-1].value, value):
            buffer.pop()

        buffer.append(new_pair)

        while buffer[0].death <= i:
            buffer.popleft()

    return _update


_docstring = """Iterator object that computes the {operation}
of a rolling window over a Python iterable.

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

Notes
-----

This method uses the algorithms outlined in [1].

[1] http://www.richardhartersworld.com/cri/2001/slidingmin.html
"""

_mindoc = _docstring.format(operation='minimum', algorithm_name='Ascending Minima')
_maxdoc = _docstring.format(operation='maximum', algorithm_name='Descending Maxima')

RollingMin = type('RollingMin', (_RollingMM,), {'_func_name': 'Min',
                    '_update': _make_update_method(ge),
                    '__doc__': _mindoc})

RollingMax = type('RollingMax', (_RollingMM,), {'_func_name': 'Max',
                    '_update': _make_update_method(le),
                    '__doc__': _maxdoc})


class RollingMin2(RollingObject):
    """Iterator object that computes the minimum value
    of a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k) (if the iterable is unordered)

    where k is the size of the rolling window

    Notes
    -----

    This method uses heap to keep track of the minimum
    value in the rolling window.

    Items that expire are lazily deleted, which can mean
    that the heap can grow to be larger than the specified
    window size, k.
    """
    _func_name = 'Min2'

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)
        self._iterator = enumerate(self._iterator)

        self._heap = [(value, i + window_size) for i, value in islice(self._iterator, window_size - 1)]
        heapq.heapify(self._heap)

    def _update(self):
        i, value = next(self._iterator)
        new_pair = (value, i + self.window_size)

        heapq.heappush(self._heap, new_pair)

        while self._heap[0][1] <= i:
            heapq.heappop(self._heap)

    def __next__(self):
        self._update()
        return self._heap[0][0]
