from collections import deque, namedtuple

from .base import RollingObject

# TODO: reduce code duplication between RollingMin and RollingMax

# Note: in the code below, the buffer size can *sometimes*
# grow beyond the size of the window. Testing suggests that for
# random arrays it never grows much larger, but I will investigate
# further and tighten the implementation.

pair = namedtuple('pair', ['value', 'death'])


class RollingMin(RollingObject):
    """Compute the minimum value in the rolling window.

    Uses the ascending minima algorithm described in [1]
    to compute each value in O(1) time and O(k) space.

    [1] http://www.richardhartersworld.com/cri/2001/slidingmin.html
    """
    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)

        self._buffer = deque([])
        self._i = 0

        # update buffer using the initial window values (there's no
        # need to check if the minimum reaches its death here)
        for _ in range(window_size - 1):
            self._update()

    def _check_death(self):
        # remove minimum values that died by the current iteration
        while self._buffer and self._buffer[0].death <= self._i:
            self._buffer.popleft()

    def _update(self):
        new_pair = pair(next(self._iterator), self._i + self.window_size)

        # value is the new minimum - overwrite the old minimum or
        # just append the value if the buffer is currently empty
        if not self._buffer or new_pair.value <= self._buffer[0].value:
            try:
                self._buffer[0] = new_pair
            except IndexError:
                self._buffer.append(new_pair)

        # value is not yet the minimum - work backwards from the
        # end of the array to find where to place it
        else:
            x = len(self._buffer) - 1
            while self._buffer[x].value >= new_pair.value:
                x -= 1
            try:
                self._buffer[x + 1] = new_pair
            except IndexError:
                self._buffer.append(new_pair)

        # finally increment the counter
        self._i += 1

    def __next__(self):
        self._check_death()
        self._update()
        return self._buffer[0].value


class RollingMax(RollingObject):
    """Compute the maximum value in the rolling window.

    Uses the descending maxima algorithm described in [1]
    to compute each value in O(1) time and O(k) space.

    [1] http://www.richardhartersworld.com/cri/2001/slidingmin.html
    """
    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)

        self._buffer = deque([])
        self._i = 0

        # update buffer using the initial window values (there's no
        # need to check if the maximum reaches its death here)
        for _ in range(window_size - 1):
            self._update()

    def _check_death(self):
        # remove maximum values that have died by the current iteration
        while self._buffer and self._buffer[0].death <= self._i:
            #print('%s dies' % str(self._buffer[0]))
            self._buffer.popleft()

    def _update(self):
        new_pair = pair(next(self._iterator), self._i + self.window_size)

        # value is the new maximum - overwrite the old maximum or
        # just append the value if the buffer is currently empty
        if not self._buffer or new_pair.value >= self._buffer[0].value:
            try:
                self._buffer[0] = new_pair
            except IndexError:
                self._buffer.append(new_pair)

        # value is not yet the maximum - work backwards from the
        # end of the array to find where to place it
        else:
            x = len(self._buffer) - 1
            while self._buffer[x].value <= new_pair.value:
                x -= 1
            try:
                self._buffer[x + 1] = new_pair
            except IndexError:
                self._buffer.append(new_pair)

        # finally increment the counter
        self._i += 1

    def __next__(self):
        self._check_death()
        self._update()
        return self._buffer[0].value
