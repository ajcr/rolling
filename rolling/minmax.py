from collections import deque, namedtuple
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

Uses the {algorithm_name} algorithm described in [1]
to compute each value in O(1) time and O(k) space.


The cost of updating the {operation} of each new
window is O(1). The memory used is O(k)
where k is the size of the window.

Parameters
----------

iterable : any iterable object
window_size : integer, the size of the rolling
    window moving over the iterable

Notes
-----

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
