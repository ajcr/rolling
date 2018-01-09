from .apply import RollingApply
from .arithmetic import RollingSum
from .logical import RollingAll, RollingAny, RollingCount
from .minmax import RollingMin, RollingMax
from .stats import RollingMean, RollingVar, RollingStd

_rolling_methods = {'Sum': RollingSum,
                    'Any': RollingAny,
                    'All': RollingAll,
                    'Count': RollingCount,
                    'Min': RollingMin,
                    'Max': RollingMax,
                    'Mean': RollingMean,
                    'Var': RollingVar,
                    'Std': RollingStd}

def rolling(iterable, window_size, func='Sum'):
    """Create a rolling iterator over an iterable object.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer
    func : callable or str, optional
        the operation to be applied to each window (default 'Sum')

    Returns
    -------

    RollingObject instance
        RollingApply if a callable was given, else a class
        instance implementing an efficient version of the
        required operation.
    """
    if callable(func):
        return RollingApply(iterable, window_size, func)
    elif isinstance(func, str):
        try:
            return _rolling_methods[func](iterable, window_size)
        except KeyError:
            raise ValueError('Unknown rolling operation')
    else:
        raise TypeError('func must be callable or str, not {}'.format(type(func)))
