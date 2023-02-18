import operator

from rolling.logical.all import All


COMPARE = {
    # (increasing, strict): cmp
    (True, True): operator.lt,
    (True, False): operator.le,
    (False, True): operator.gt,
    (False, False): operator.ge,
}


class Monotonic(All):
    """
    Rolling monotonicity.

    Indicates if the values in the window are monotonically
    increasing or monotically decreasing (i.e. in sorted
    order).

    Parameters
    ----------

    iterable : iterable of comparable objects
    window_size : integer, the size of the rolling
        window moving over the iterable
    window_type : str, "fixed" or "variable"
    increasing : bool : default is True
    strict : bool : if True, inequalities are strict
    initial : Any : value to use for initial comparison
        if not given, defaults to negative/positive inf
        for increasing/decreasing monotonicity

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(1)

    Examples
    --------

    >>> import rolling
    >>> r_mono = rolling.Monotonic([1,2,3,4,3,2,1], 3, increasing=False))
    >>> list(r_mono)
    [False, False, False, True, True]
    """

    def __init__(
        self,
        iterable,
        window_size,
        window_type="fixed",
        increasing=True,
        strict=False,
        initial=None,
    ):
        self._compare = COMPARE[(increasing, strict)]

        if initial is None:
            self._previous = -float("inf") if increasing else float("inf")
        else:
            self._previous = initial

        super().__init__(iterable, window_size, window_type)

    def _add_new(self, new):
        new_ = self._compare(self._previous, new)
        super()._add_new(new_)
        self._previous = new

    def _update_window(self, new):
        new_ = self._compare(self._previous, new)
        super()._update_window(new_)
        self._previous = new

    @property
    def current_value(self):
        return self._i - self._window_obs >= self._last_false - 1
