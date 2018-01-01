from .arithmetic import RollingSum


class RollingMean(RollingSum):
    """Compute the mean value of a rolling window.

    The cost of updating the mean is O(1), and the
    O(k) space is required.
    """
    def __next__(self):
        self._update()
        return self._sum / self.window_size
