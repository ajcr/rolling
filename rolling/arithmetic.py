from collections import Counter, deque
from itertools import islice

from .base import RollingObject


class RollingSum(RollingObject):

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)

        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)
        self._buffer.appendleft(0)
        self._sum = sum(self._buffer)

    def _update(self):
        value = next(self._iterator)
        self._sum += value - self._buffer.popleft()
        self._buffer.append(value)

    def __next__(self):
        self._update()
        return self._sum



class RollingNunique(RollingObject):

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)
        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)
        self._counter = Counter(self._buffer)
        self._nunique = len(self._counter)

    def _update(self):
        n = next(self._iterator)
        out = self._buffer.popleft()
        self._counter[out] -= 1
        if self._counter[out] == 0:
            del self._counter[out]

    def __next__(self):
        self._update()
        return len(self._counter)



