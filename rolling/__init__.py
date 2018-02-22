from .apply import Apply
from .arithmetic import Sum
from .base import RollingObject
from .logical import All, Any
from .minmax import Min, Max, MinHeap
from .stats import Mean, Var, Std, Median

def _get_subclasses(cls):
    # https://stackoverflow.com/a/33607093/3923281
    for subclass in cls.__subclasses__():
        yield from _get_subclasses(subclass)
        yield subclass

_rolling_methods = {cls.__name__: cls for cls in _get_subclasses(RollingObject)}

def rolling(iterable, window_size, operation='Sum', window_type='fixed', **kwargs):
    """Create a rolling iterator over an iterable object to
    perform the specified function.

    Parameters
    ----------

    iterable : any iterable object

    window_size : integer

    operation : callable or str, default 'Sum'
        the operation to be applied to each window (default 'Sum')
        passing one of the following strings returns a RollingObject
        subclass instance implementing the operation efficiently:
            - 'Sum', sum of values
            - 'Any', true if any value is true, else false
            - 'All', true if all values are true, else false
            - 'Min', minimum value
            - 'MinHeap', minimum value, uses heap not deque to track values
            - 'Max', maximum value
            - 'Mean', mean value
            - 'Median', median value
            - 'Var', variance of values
            - 'Std', standard deviation of values

        if a callable object is passed instead of a string, an instance
        of the Apply class will be returned using that callable as the
        window operation

    window_type : str, default 'fixed'
        determines whether the window size is constant ('fixed')
        or if fewer values are permitted in the window as it rolls
        on and off the iterable ('variable')

    Returns
    -------

    RollingObject subclass instance
        Apply instance if a callable was given as the operation, else
        a class instance implementing an efficient version of the
        required operation.
    """
    if callable(operation):
        return Apply(iterable, window_size, operation=operation, window_type=window_type, **kwargs)
    elif isinstance(operation, str):
        try:
            return _rolling_methods[operation](iterable, window_size, window_type=window_type, **kwargs)
        except KeyError:
            raise ValueError('Unknown rolling operation: \'{}\''.format(operation))
    else:
        raise TypeError('operation must be callable or str, not {}'.format(type(operation).__name__))
