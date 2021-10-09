from collections import deque
from heapq import heapify, heappush, heappop
from itertools import islice
from operator import itemgetter

from .base import RollingObject

# A tuple in a window has a value and an index at which it will exit the window
_value = itemgetter(0)
_death = itemgetter(1)


class Min(RollingObject):
    """
    Iterator object that computes the minimum
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

    This method uses the algorithms outlined in [1] to
    maintain a deque of ascending minima.

    [1] http://www.richardhartersworld.com/cri/2001/slidingmin.html

    """

    # Note: _obs must be tracked separately, we cannot just use
    # the size of the buffer as the algorithm may overwrite existing
    # values with a new value, rather than appending the value

    def _init_fixed(self, iterable, window_size, **kwargs):
        self._i = -1
        self._obs = 0
        self._buffer = deque()
        for new in islice(self._iterator, window_size - 1):
            self._add_new(new)

    def _init_variable(self, iterable, window_size, **kwargs):
        self._i = -1
        self._obs = 0
        self._buffer = deque()

    def _update_window(self, new):
        self._i += 1
        new_pair = (new, self._i + self.window_size)
        # remove larger values from the end of the buffer
        while self._buffer and _value(self._buffer[-1]) >= new:
            self._buffer.pop()
        self._buffer.append(new_pair)
        # remove any minima that die on this iteration
        if _death(self._buffer[0]) <= self._i:
            self._buffer.popleft()

    def _add_new(self, new):
        self._i += 1
        self._obs += 1
        new_pair = (new, self._i + self.window_size)
        # remove larger values from the end of the buffer
        while self._buffer and _value(self._buffer[-1]) >= new:
            self._buffer.pop()
        self._buffer.append(new_pair)

    def _remove_old(self):
        self._i += 1
        self._obs -= 1
        # remove any minima that die on this iteration
        while _death(self._buffer[0]) <= self._i:
            self._buffer.popleft()

    @property
    def current_value(self):
        return _value(self._buffer[0])


class Max(RollingObject):
    """
    Iterator object that computes the maximum
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

    This method uses the algorithms outlined in [1] to
    maintain a deque of descending maxima.

    [1] http://www.richardhartersworld.com/cri/2001/slidingmin.html

    """

    # Note: _obs must be tracked separately, we cannot just use
    # the size of the buffer as the algorithm may overwrite existing
    # values with a new value, rather than appending the value

    def _init_fixed(self, iterable, window_size, **kwargs):
        self._i = -1
        self._obs = 0
        self._buffer = deque()
        for new in islice(self._iterator, window_size - 1):
            self._add_new(new)

    def _init_variable(self, iterable, window_size, **kwargs):
        self._buffer = deque()
        self._i = -1
        self._obs = 0

    def _update_window(self, new):
        self._i += 1
        new_pair = (new, self._i + self.window_size)
        # remove smaller values from the end of the buffer
        while self._buffer and _value(self._buffer[-1]) <= new:
            self._buffer.pop()
        self._buffer.append(new_pair)
        # remove any maxima that die on this iteration
        if _death(self._buffer[0]) <= self._i:
            self._buffer.popleft()

    def _add_new(self, new):
        self._i += 1
        self._obs += 1
        new_pair = (new, self._i + self.window_size)
        # remove smaller values from the end of the buffer
        while self._buffer and _value(self._buffer[-1]) <= new:
            self._buffer.pop()
        self._buffer.append(new_pair)

    def _remove_old(self):
        self._i += 1
        self._obs -= 1
        # remove any maxima that die on this iteration
        while _death(self._buffer[0]) <= self._i:
            self._buffer.popleft()

    @property
    def current_value(self):
        return _value(self._buffer[0])


class MinHeap(RollingObject):
    """
    Iterator object that computes the minimum value
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
    values in the rolling window (as opposed to a deque
    used by the Min class).

    Items that expire are lazily deleted, which can mean
    that the heap can grow to be larger than the specified
    window size, k, in cases where data is ordered.
    """

    def _init_fixed(self, iterable, window_size, **kwargs):
        head = islice(self._iterator, window_size - 1)
        # faster to create the heap this way, rather than repeat _add_new()
        self._heap = [(value, i + window_size) for i, value in enumerate(head)]
        heapify(self._heap)
        self._i = len(self._heap) - 1
        self._obs = len(self._heap)

    def _init_variable(self, iterable, window_size, **kwargs):
        self._heap = []
        self._i = -1
        self._obs = 0

    def _update_window(self, new):
        self._i += 1
        new_pair = (new, self._i + self.window_size)
        heappush(self._heap, new_pair)
        # remove any minima that die on this iteration
        while _death(self._heap[0]) <= self._i:
            heappop(self._heap)

    def _add_new(self, new):
        self._i += 1
        self._obs += 1
        new_pair = (new, self._i + self.window_size)
        heappush(self._heap, new_pair)

    def _remove_old(self):
        self._i += 1
        self._obs -= 1
        # remove any minima that die on this iteration
        while _death(self._heap[0]) <= self._i:
            heappop(self._heap)

    @property
    def current_value(self):
        return _value(self._heap[0])
