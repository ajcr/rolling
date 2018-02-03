import abc


class RollingObject(metaclass=abc.ABCMeta):
    """Baseclass for rolling iterator objects.

    All child classes must implement the following:
        -
        -
    """
    def __new__(cls, iterable, *args, window_type='fixed', **kwargs):
        if window_type == 'fixed':
            cls.__init__ = cls._init_fixed
            cls.__next__ = cls._next_fixed
        elif window_type == 'variable':
            cls.__init__ = cls._init_variable
            cls.__next__ = cls._next_variable
        else:
            raise ValueError("Unknown window_type '{}'".format(window_type))
        cls.window_type = window_type
        return super().__new__(cls)

    def __init__(self, iterable, window_size, *args, **kwargs):
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

    @abc.abstractproperty
    def current_value(self):
        'return the current value of the window'
        pass

    @abc.abstractmethod
    def _init_fixed(self):
        'intialise as a fixed-size window'
        pass

    @abc.abstractmethod
    def _init_variable(self):
        'intialise as a variable-size window'
        pass

    @abc.abstractmethod
    def _remove_old(self):
        'remove the oldest value from the window'
        pass

    @abc.abstractmethod
    def _add_new(self):
        'take a new value from the iterator and it to the window'
        pass

    @abc.abstractmethod
    def _update(self):
        'simultaneously add a new value and remove the old value'
        pass

    @staticmethod
    def _validate_window_size(k):
        "Check the passed value is a positive integer"
        if not isinstance(k, int):
            raise TypeError('window_size must be integer type, got {}'.format(type(k).__name__))
        if k <= 0:
            raise ValueError('window_size must be positive')
        return k
