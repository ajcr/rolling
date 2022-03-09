from rolling.arithmetic import Sum


class Mean(Sum):
    """
    Iterator object that computes the mean of
    a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k)

    where k is the size of the rolling window

    """

    @property
    def current_value(self):
        return self._sum / self._obs
