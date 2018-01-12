import abc


class RollingObject(metaclass=abc.ABCMeta):
    """Baseclass for rolling iterator objects.

    Note: this is an abc mainly just to enforce
    classes to consistently implement a couple
    of basic methods needed for iteration.
    """
    def __init__(self, iterable, window_size):
        self.window_size = self._validate_window_size(window_size)
        self._iterator = iter(iterable)

    def __repr__(self):
        if hasattr(self, '_func_name'):
            name = self._func_name
        else:
            name = self._func.__name__
        return "Rolling(func='{}', window_size={})".format(name, self.window_size)

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

    @staticmethod
    def _validate_window_size(k):
        "Check the passed value is a positive integer"
        if not isinstance(k, int):
            raise TypeError('window_size must be integer type, got {}'.format(type(k).__name__))
        if k <= 0:
            raise ValueError('window_size must be positive')
        return k
