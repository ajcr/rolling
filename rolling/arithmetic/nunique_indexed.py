from collections import Counter, deque

from rolling.base_indexed import RollingIndexed

class NuniqueIndexed(RollingIndexed):
    """
    Iterator object that counts the number of unique values in a rolling
    window with an index array

    Parameters
    ----------
    
    index : the object that will serve as index
    iterable : any iterable object
    window_size : same type as the index, the maximum size (difference between indices)
        of the rolling window moving over the iterable
    
    Complexity
    ----------
    
    Update time: O(1)
    Memory usage: O(k)
    
    where k is the size of the rolling window (which can potentially be n)

    """

    def __init__(self, index, iterable, window_size, window_type="variable"):
        self._idx_buffer = deque()
        self._val_buffer = deque()
        self._counter = Counter()
        self._nunique = 0
        super().__init__(index, iterable, window_size, window_type)

    def _init_variable(self, **kwargs):
        pass

    def _insert(self, idx, val):
        assert not self._idx_buffer or self._idx_buffer[0] <= idx, \
            "Indices should be monotonic"

        self._idx_buffer.append(idx)
        self._val_buffer.append(val)
        if self._counter[val] == 0:
            self._nunique += 1
        self._counter[val] += 1

        assert len(self._idx_buffer) == len(self._val_buffer), \
            "Both buffers should have same length"

    def _evict(self, idx):
        """ Removes all values whose index is lower or equal than idx
        """
        # Keep advancing both iterators until smallest is greater than idx
        while self._idx_buffer and self._idx_buffer[0] <= idx:
            self._idx_buffer.popleft()
            val = self._val_buffer.popleft()

            self._counter[val] -= 1
            if self._counter[val] == 0:
                self._nunique -= 1

        assert len(self._idx_buffer) == len(self._val_buffer), \
            "Both buffers should have same length"

    @property
    def current_value(self):
        return self._nunique

    @property
    def _obs(self):
        return self._idx_buffer[-1] - self._idx_buffer[0]