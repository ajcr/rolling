import abc
from itertools import chain


class RollingObject(metaclass=abc.ABCMeta):
    """
    Baseclass for rolling iterator objects.

    All iteration logic is handled in this class.
    Subclasses implement methods manipulating
    the attributes needed to compute the value of
    the rolling window as values are added and removed.

    Subclasses *must* implement the following methods
    with the following parameters:

      _init_fixed(self, iterable, window_size, **kwargs)
      _init_variable(self, iterable, window_size, **kwargs)
      _update_window(self, new)
      _add_new(self, new)
      _remove_old(self)
      current_value(self)

    Variable-length instances must also have a self._obs
    attribute that returns the current size of the window.

    """
    def __init__(self, iterable, window_size, window_type="fixed", **kwargs):
        self.window_type = window_type
        self.window_size = _validate_window_size(window_size)
        self._iterator = iter(iterable)
        self._filled = self.window_type == "fixed"

        if window_type == "fixed":
            self._init_fixed(iterable, window_size, **kwargs)

        elif window_type == "variable":
            self._init_variable(iterable, window_size, **kwargs)

        else:
            raise ValueError("Unknown window_type '{}'".format(window_type))

    def __repr__(self):
        return "Rolling(operation='{}', window_size={}, window_type='{}')".format(
            self.__class__.__name__, self.window_size, self.window_type
        )

    def __iter__(self):
        return self

    def __next__(self):

        if self.window_type == "fixed":
            new = next(self._iterator)
            self._update_window(new)
            return self.current_value

        elif self.window_type == "variable":
            # while the window size is not reached, add new values
            if not self._filled and self._obs < self.window_size:
                new = next(self._iterator)
                self._add_new(new)
                if self._obs == self.window_size:
                    self._filled = True
                return self.current_value

            # once the window size is reached, update until the iterator finishes
            try:
                new = next(self._iterator)
                self._update_window(new)
                return self.current_value

            # if the iterator finishes, remove the oldest values one at a time
            except StopIteration:
                if self._obs == 1:
                    raise
                else:
                    self._remove_old()
                    return self.current_value

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
        raise TypeError(
            "window_size must be integer type, got {}".format(type(k).__name__)
        )
    if k <= 0:
        raise ValueError("window_size must be positive")
    return k
