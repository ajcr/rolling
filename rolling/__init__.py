from .apply import Apply
from .arithmetic import Sum
from .base import RollingObject
from .logical import All, Any, Count
from .minmax import Min, Max, Min2
from .stats import Mean, Var, Std, Median

def _get_subclasses(cls):
    # https://stackoverflow.com/a/33607093/3923281
    for subclass in cls.__subclasses__():
        yield from _get_subclasses(subclass)
        yield subclass

_rolling_methods = {cls.__name__: cls for cls in _get_subclasses(RollingObject)}

def rolling(iterable, window_size, func='Sum', window_type='fixed', **kwargs):
    """Create a rolling iterator over an iterable object to
    perform the specified function.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer
    func : callable or str, default 'Sum'
        the operation to be applied to each window (default 'Sum')
            - 'Sum', sum of values
            - 'Any', true if any value is true, else false
            - 'All', true if all values are true, else false
            - 'Count', count of true values
            - 'Min', minimum value
            - 'Min2', minimum value, uses heap not deque to track values
            - 'Max', maximum value
            - 'Mean', mean value
            - 'Median', median value
            - 'Var', variance of values
            - 'Std', standard deviation of values
    window_type : str, default 'fixed'
        determines whether the window size is constant ('fixed')
        or if fewer values are permitted in the window as it rolls
        on and off the iterable ('variable')

    Returns
    -------

    RollingObject subclass instance
        RollingApply if a callable was given, else a class
        instance implementing an efficient version of the
        required operation.
    """
    if callable(func):
        return Apply(iterable, window_size, func=func, window_type=window_type, **kwargs)
    elif isinstance(func, str):
        try:
            return _rolling_methods[func](iterable, window_size, window_type=window_type, **kwargs)
        except KeyError:
            raise ValueError('Unknown rolling operation: \'{}\''.format(func))
    else:
        raise TypeError('func must be callable or str, not {}'.format(type(func).__name__))
