import abc
from collections.abc import Iterator

class RollingIndexed(Iterator):
    """
    Baseclass for rolling iterators over _indexed_ or sparse data
    """

    def __init__(self, index, iterable, window_size, window_type="variable", **kwargs):
        """Initialize a base rolling indexed class

        Args:
            index: Must be a monotonic array of the same type that `window_size`,
                it must support the (-) operator.
            iterable: Any iterable, must be same length as index
            window_size: Max difference between the first and last index of the
                stored elements
            window_type (str, optional): Defaults to "variable".

        Raises:
            ValueError: _description_
        """
        self.window_type = window_type
        
        assert len(index) == len(iterable), \
            "Index and values should have same size"

        self._iterator_index = iter(index)
        self._iterator_values = iter(iterable)
        self.window_size = window_size

        if window_type == "variable":
            self._init_variable(**kwargs)

        else:
            raise ValueError(f"Unknown window_type '{window_type}'")

    def _next_variable(self):
        newidx = next(self._iterator_index)
        newval = next(self._iterator_values)

        self._insert(newidx, newval)
        self._evict(newidx - self.window_size)
            
        return self.current_value

    def __next__(self):
        if self.window_type == "variable":
            return self._next_variable()
        
        raise NotImplementedError(f"next() not implemented for {self.window_type}")

    @abc.abstractmethod
    def _insert(self, idx, val):
        """ Inserts value into the window with index idx. idx is greater that 
            all indexes received
        """

    @abc.abstractmethod
    def _evict(self, idx):
        """ Removes all values whose index is lower or equal than idx
        """

    @property
    @abc.abstractmethod
    def current_value(self):
        """
        Return the current value of the window
        """
        pass

    @abc.abstractmethod
    def _init_variable(self, **kwargs):
        """
        Intialise as a variable-size window
        """
        pass

    @property
    @abc.abstractmethod
    def _obs(self):
        """
        Return the window size
        """
        pass

    def __repr__(self):
        return "RollingIndexed(operation='{}', window_size={}, window_type='{}')".format(
            self.__class__.__name__, self.window_size, self.window_type
        )
