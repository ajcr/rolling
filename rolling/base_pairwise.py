import abc
from collections.abc import Iterator
from itertools import chain


class RollingPairwise(Iterator):
    """
    Baseclass for rolling iterators over two iterables.

    """
    def __init__(self, iterable_1, iterable_2, window_size, window_type="fixed", **kwargs):
        self.window_type = window_type
        self.window_size = _validate_window_size(window_size)
        self._iterator_1 = iter(iterable_1)
        self._iterator_2 = iter(iterable_2)
        self._filled = self.window_type == "fixed"

        if window_type == "fixed":
            self._init_fixed(**kwargs)

        elif window_type == "variable":
            self._init_variable(**kwargs)

        else:
            raise ValueError(f"Unknown window_type '{window_type}'")

    def __repr__(self):
        return "RollingPairwise(operation='{}', window_size={}, window_type='{}')".format(
            self.__class__.__name__, self.window_size, self.window_type
        )

    def _next_fixed(self):
        new_1 = next(self._iterator_1)
        new_2 = next(self._iterator_2)
        self._update_window(new_1, new_2)
        return self.current_value

    def _next_variable(self):
        # while the window size is not reached, add new values
        if not self._filled and self._obs < self.window_size:
            new_1 = next(self._iterator_1)
            new_2 = next(self._iterator_2)
            self._add_new(new_1, new_2)
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

    def __next__(self):

        if self.window_type == "fixed":
            return self._next_fixed()

        if self.window_type == "variable":
            return self._next_variable()

        raise NotImplementedError(f"next() not implemented for {self.window_type}")

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
    def _init_fixed(self, **kwargs):
        """
        Intialise as a fixed-size window
        """
        pass

    @abc.abstractmethod
    def _init_variable(self, **kwargs):
        """
        Intialise as a variable-size window
        """
        pass

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


def _validate_window_size(k):
    """
    Check if k is a positive integer
    """
    if not isinstance(k, int):
        raise TypeError(f"window_size must be integer type, got {type(k).__name__}")
    if k <= 0:
        raise ValueError("window_size must be positive")
    return k
