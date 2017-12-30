import abc


class RollingObject(metaclass=abc.ABCMeta):
    """Baseclass for rolling iterator objects.

    Note: this is an abc mainly just to enforce
    classes to consistently implement a couple
    of basic methods needed for iteration.
    """
    def __init__(self, iterable, window_size):
        self.window_size = window_size
        self._iterator = iter(iterable)

    def __repr__(self):
        return "RollingObject(func='{}', window_size={})".format(
                (getattr(self, 'func', None) or self.__class__).__name__,
                self.window_size)

    def __iter__(self):
        return self

    @abc.abstractmethod
    def _update(self):
        # roll window forward and update variables
        pass

    @abc.abstractmethod
    def __next__(self):
        # call self.update() and return value
        pass
