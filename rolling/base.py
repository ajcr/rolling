import abc
from collections import deque
from collections.abc import Iterator
from itertools import chain


class RollingObject(Iterator):
    """
    Baseclass for rolling iterator objects.

    All iteration logic for 'fixed', 'variable' and
    'indexed' window types is handled by this class.

    Subclasses of RollingObject must implement methods
    to initialize and manipulate any attributes needed
    to compute the window value as it rolls across the
    given iterable.

    These methods are:

     * _init_fixed()     fixed window initialization
     * _init_variable()  variable window initialization
     * _update_window()  add new value, remove oldest value
     * _add_new()        add new value (increase size)
     * _remove_old()     remove oldest value (decrease size)

    The following @property methods must also be implemented:

     * _obs              number of observations in window
     * current_value     current value of operation on window

    """

    def __init__(self, iterable, window_size, window_type="fixed", **kwargs):
        self.window_type = window_type
        self.window_size = _validate_window_size(window_size, window_type)
        self._iterator = iter(iterable)
        self._filled = self.window_type == "fixed"

        if window_type == "fixed":
            self._init_fixed(iterable, window_size, **kwargs)

        elif window_type == "variable":
            self._init_variable(iterable, window_size, **kwargs)

        elif window_type == "indexed":
            # keep track of all indexes that we encounter. Assumes that all
            # values we encounter will be stored in the same order. If not,
            # the subtype will need to implement its own _next_indexed() method.
            self._index_buffer = deque()
            self._init_indexed(iterable, window_size, **kwargs)

        else:
            raise ValueError(f"Unknown window_type '{window_type}'")

    def __repr__(self):
        return "Rolling(operation='{}', window_size={}, window_type='{}')".format(
            self.__class__.__name__, self.window_size, self.window_type
        )

    def _next_fixed(self):
        new = next(self._iterator)
        self._update_window(new)
        return self.current_value

    def _next_variable(self):
        # while the window size is not reached, add new values
        if not self._filled and self._obs < self.window_size:
            new = next(self._iterator)
            self._add_new(new)
            self._filled = self._obs == self.window_size
            return self.current_value

        # once the window size is reached, consider fixed until iterator ends
        try:
            return self._next_fixed()

        # if the iterator finishes, remove the oldest values one at a time
        except StopIteration:
            if self._obs == 1:
                raise
            else:
                self._remove_old()
                return self.current_value

    def _next_indexed(self):
        new_index, new_value = next(self._iterator)

        if self._index_buffer and new_index < self._index_buffer[-1]:
            raise ValueError(
                "Next index must be greater than or equal to last added index: "
                f"{new_index} < {self._index_buffer[0]}"
            )

        self._index_buffer.append(new_index)
        self._add_new(new_value)

        min_index = new_index - self.window_size

        while self._index_buffer and self._index_buffer[0] <= min_index:
            self._remove_old()
            self._index_buffer.popleft()

        return self.current_value

    def __next__(self):

        if self.window_type == "fixed":
            return self._next_fixed()

        if self.window_type == "variable":
            return self._next_variable()

        if self.window_type == "indexed":
            return self._next_indexed()

        raise NotImplementedError(f"next() not implemented for {self.window_type}")

    def extend(self, iterable):
        """
        Extend the iterator being consumed with a new iterable.

        The extend() method may be called at any time (even after
        StopIteration has been raised). The most recent values from
        the current iterator are retained and used in the calculation
        of the next window value.

        For "variable" windows which are decreasing in size, extending
        the iterator means that these windows will grow towards their
        maximum size again.

        """
        self._iterator = chain(self._iterator, iterable)

        if self.window_type == "variable":
            self._filled = False

    @property
    @abc.abstractmethod
    def current_value(self):
        """
        Return the current value of the window
        """
        pass

    @property
    @abc.abstractmethod
    def _obs(self):
        """
        Return the number of observations in the window
        """
        pass

    @abc.abstractmethod
    def _init_fixed(self):
        """
        Intialise as a fixed-size window
        """
        pass

    @abc.abstractmethod
    def _init_variable(self):
        """
        Intialise as a variable-size window
        """
        pass

    def _init_indexed(self, *args, **kwargs):
        """
        Intialise as an indexed window.

        In most cases this is the same as initialising a variable-size window.
        """
        return self._init_variable(*args, **kwargs)

    @abc.abstractmethod
    def _remove_old(self):
        """
        Remove the oldest value from the window, decreasing window size by 1
        """
        pass

    @abc.abstractmethod
    def _add_new(self, new):
        """
        Add a new value to the window, increasing window size by 1
        """
        pass

    @abc.abstractmethod
    def _update_window(self, new):
        """
        Add a new value to the window and remove the oldest value from the window
        """
        pass


def _validate_window_size(window_size, window_type):
    """
    Check if k is a positive integer
    """
    if window_type in {"fixed", "variable"}:
        if not isinstance(window_size, int):
            raise TypeError(f"window_size must be integer type, got {type(window_size).__name__}")
        if window_size <= 0:
            raise ValueError("window_size must be positive")
    return window_size
