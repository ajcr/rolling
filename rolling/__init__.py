from .apply import RollingApply
from .arithmetic import RollingSum
from .base import RollingObject
from .logical import RollingAll, RollingAny, RollingCount
from .minmax import RollingMin, RollingMax, RollingMin2
from .stats import RollingMean, RollingVar, RollingStd, RollingMedian

def _get_subclasses(cls):
    # https://stackoverflow.com/a/33607093/3923281
    for subclass in cls.__subclasses__():
        yield from _get_subclasses(subclass)
        yield subclass

_rolling_methods = {cls._func_name: cls for cls in _get_subclasses(RollingObject)
                        if hasattr(cls, '_func_name')}

def rolling(iterable, window_size, func='Sum', window_type='fixed'):
    """Create a rolling iterator over an iterable object.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer
    func : callable or str, optional
        the operation to be applied to each window (default 'Sum')
            - 'Sum', sum of values
            - 'Any', true if any value if true, else false
            - 'All', true if all values are true, else false
            - 'Count', count of true values
            - 'Min', minimum value, ascending minima algorithm
            - 'Min2', minimum value, heap-based algorithm
            - 'Max', maximum value, descending maxima algorithm
            - 'Mean', mean value
            - 'Median', median value
            - 'Var', variance of values
            - 'Std', standard deviation of values
    window_type : str [default 'fixed']
        indicates whether the window size is constant ('fixed')
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
        return RollingApply(iterable, window_size, func, window_type=window_type)
    elif isinstance(func, str):
        try:
            return _rolling_methods[func](iterable, window_size, window_type=window_type)
        except KeyError:
            raise ValueError('Unknown rolling operation')
    else:
        raise TypeError('func must be callable or str, not {}'.format(type(func)))
