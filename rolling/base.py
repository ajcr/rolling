import abc


class RollingObject(metaclass=abc.ABCMeta):
    """Baseclass for rolling iterator objects.

    The __new__ method sets the appropriate magic
    methods upon class creation.

    All iteration logic is handled in this class:
    subclasses just implement methods manipulating
    any attributes needed to compute their rolling
    operation as the iteration progresses.

    All subclasses *must* implement the following methods
    with the following call signatures:

        _init_fixed(self, iterable, window_size, **kwargs)
        _init_variable(self, iterable, window_size, **kwargs)
        _update_window(self, new)
        _add_new(self, new)
        _remove_old(self)
        current_value(self) [this is a @property]

    Note: variable-length instances must also have a self._obs
    attribute to return the current size of the variable-length
    window.
    """
    def __new__(cls, iterable, window_size, window_type='fixed', **kwargs):
        if window_type == 'fixed':
            cls.__init__ = cls._init_fixed
            cls.__next__ = cls._next_fixed
        elif window_type == 'variable':
            cls.__init__ = cls._init_variable
            cls.__next__ = cls._next_variable
        else:
            raise ValueError("Unknown window_type '{}'".format(window_type))
        # create instance and initialise attributes
        self = super().__new__(cls)
        self.window_type = window_type
        self.window_size = self._validate_window_size(window_size)
        self._iterator = iter(iterable)
        if self.window_type == 'variable':
            self._filled = False
        return self

    def __repr__(self):
        return "Rolling(operation='{}', window_size={}, window_type='{}')".format(
                    self.__class__.__name__, self.window_size, self.window_type)

    def __iter__(self):
        return self

    def _next_fixed(self):
        'return the next value for fixed-length windows'
        new = next(self._iterator)
        self._update_window(new)
        return self.current_value

    def _next_variable(self):
        'return the next value for variable-length windows'
        # while the window size is not reached, add new values
        if not self._filled and self._obs < self.window_size:
            new = next(self._iterator)
            self._add_new(new)
            if self._obs == self.window_size:
                self._filled = True
            return self.current_value
        # once the window size is reached, update window until the iterator finishes
        try:
            new = next(self._iterator)
            self._update_window(new)
            return self.current_value
        except StopIteration:
            # if the iterator finishes, remove the oldest values one by one
            if self._obs == 1:
                raise
            else:
                self._remove_old()
                return self.current_value

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
        'remove the oldest value from the window, decreasing window size by 1'
        pass

    @abc.abstractmethod
    def _add_new(self, new):
        'add a new value to the window, increasing window size by 1'
        pass

    @abc.abstractmethod
    def _update_window(self, new):
        'add a new value to the window and remove the oldest value from the window'
        pass

    @staticmethod
    def _validate_window_size(k):
        'check if k is a positive integer'
        if not isinstance(k, int):
            raise TypeError('window_size must be integer type, got {}'.format(type(k).__name__))
        if k <= 0:
            raise ValueError('window_size must be positive')
        return k
