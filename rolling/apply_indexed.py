from collections import deque

from .base_indexed import RollingIndexed

class ApplyIndexed(RollingIndexed):
    """
    Apply a function to windows over an indexed array

    Parameters
    ----------
    
    index : the object that will serve as index
    iterable : any iterable object
    window_size : same type as the index, the maximum size (difference between indices)
        of the rolling window moving over the iterable
    function : callable, the function to be applied to the current window of each
        iterable
    """

    def __init__(self, index, iterable, window_size, function, window_type="variable"):
        self._idx_buffer = deque()
        self._val_buffer = deque()
        self._function = function
        super().__init__(index, iterable, window_size, window_type)

    @property
    def current_value(self):
        return self._function(self._val_buffer)

    def _init_variable(self, **kwargs):
        pass

    def _insert(self, idx, val):
        assert not self._idx_buffer or self._idx_buffer[0] <= idx, \
            "Indices should be monotonic"

        self._idx_buffer.append(idx)
        self._val_buffer.append(val)

        assert len(self._idx_buffer) == len(self._val_buffer), \
            "Both buffers should have same length"

    def _evict(self, idx):
        """ Removes all values whose index is lower or equal than idx
        """
        # Keep advancing both iterators until smallest is greater than idx
        while self._idx_buffer and self._idx_buffer[0] <= idx:
            self._idx_buffer.popleft()
            self._val_buffer.popleft()

        assert len(self._idx_buffer) == len(self._val_buffer), \
            "Both buffers should have same length"

    @property
    def _obs(self):
        return self._idx_buffer[-1] - self._idx_buffer[0]

    def __repr__(self):
        return "ApplyIndexed(operation='{}', window_size={}, window_type='{}')".format(
            self._function.__name__, self.window_size, self.window_type
        )