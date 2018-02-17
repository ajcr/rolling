from collections import deque, namedtuple
import heapq
from itertools import islice

from .base import RollingObject

pair = namedtuple('pair', ['value', 'death'])

# todo: reduce code duplication in the classes below

class RollingMin(RollingObject):
    """Iterator object that computes the minimum
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

    # Note: _obs must be tracked separately, we cannot just use
    # the size of the buffer as the algorithm may overwrite existing
    # values with a new value, rather than appending the value

    _func_name = 'Min'

    def _init_fixed(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        head = islice(self._iterator, window_size - 1)
        self._i = -1
        self._obs = 0
        self._buffer = deque()
        for value in head:
            self._i += 1
            self._obs += 1
            new_pair = pair(value, self._i + self.window_size)
            while self._buffer and self._buffer[-1].value >= value:
                self._buffer.pop()
            self._buffer.append(new_pair)

    def _init_variable(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        self._buffer = deque()
        self._i = -1
        self._obs = 0

    def _update(self):
        value = next(self._iterator)
        self._i += 1
        new_pair = pair(value, self._i + self.window_size)
        while self._buffer and self._buffer[-1].value >= value:
            self._buffer.pop()
        self._buffer.append(new_pair)
        while self._buffer[0].death <= self._i:
            self._buffer.popleft()

    def _add_new(self):
        value = next(self._iterator)
        self._i += 1
        self._obs += 1
        new_pair = pair(value, self._i + self.window_size)
        while self._buffer and self._buffer[-1].value >= value:
            self._buffer.pop()
        self._buffer.append(new_pair)

    def _remove_old(self):
        self._i += 1
        self._obs -= 1
        while self._buffer[0].death <= self._i:
            self._buffer.popleft()

    @property
    def current_value(self):
        return self._buffer[0].value


class RollingMax(RollingObject):
    """Iterator object that computes the maximum
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

    # Note: _obs must be tracked separately, we cannot just use
    # the size of the buffer as the algorithm may overwrite existing
    # values with a new value, rather than appending the value

    _func_name = 'Max'

    def _init_fixed(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        head = islice(self._iterator, window_size - 1)
        self._i = -1
        self._obs = 0
        self._buffer = deque()
        for value in head:
            self._i += 1
            self._obs += 1
            new_pair = pair(value, self._i + self.window_size)
            while self._buffer and self._buffer[-1].value <= value:
                self._buffer.pop()
            self._buffer.append(new_pair)

    def _init_variable(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        self._buffer = deque()
        self._i = -1
        self._obs = 0

    def _update(self):
        value = next(self._iterator)
        self._i += 1
        new_pair = pair(value, self._i + self.window_size)
        while self._buffer and self._buffer[-1].value <= value:
            self._buffer.pop()
        self._buffer.append(new_pair)
        while self._buffer[0].death <= self._i:
            self._buffer.popleft()

    def _add_new(self):
        value = next(self._iterator)
        self._i += 1
        self._obs += 1
        new_pair = pair(value, self._i + self.window_size)
        while self._buffer and self._buffer[-1].value <= value:
            self._buffer.pop()
        self._buffer.append(new_pair)

    def _remove_old(self):
        self._i += 1
        self._obs -= 1
        while self._buffer[0].death <= self._i:
            self._buffer.popleft()

    @property
    def current_value(self):
        return self._buffer[0].value


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

    This method uses a heap to keep track of the minimum
    value in the rolling window.

    Items that expire are lazily deleted, which can mean
    that the heap can grow to be larger than the specified
    window size, k.
    """
    _func_name = 'Min2'

    def _init_fixed(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        head = islice(self._iterator, window_size - 1)
        self._heap = [pair(value, i + window_size) for i, value in enumerate(head)]
        heapq.heapify(self._heap)
        self._i = len(self._heap) - 1
        self._obs = len(self._heap)

    def _init_variable(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        self._heap = []
        self._i = -1
        self._obs = 0

    def _update(self):
        value = next(self._iterator)
        self._i += 1
        new_pair = pair(value, self._i + self.window_size)
        heapq.heappush(self._heap, new_pair)
        while self._heap[0].death <= self._i:
            heapq.heappop(self._heap)

    def _add_new(self):
        value = next(self._iterator)
        self._i += 1
        self._obs += 1
        new_pair = pair(value, self._i + self.window_size)
        heapq.heappush(self._heap, new_pair)

    def _remove_old(self):
        self._i += 1
        self._obs -= 1
        while self._heap[0].death <= self._i:
            heapq.heappop(self._heap)

    @property
    def current_value(self):
        return self._heap[0].value
