from collections import Counter
from math import sqrt
from statistics import variance, stdev, mean as _mean, median as _median

import pytest

from rolling.apply import Apply
from rolling.stats import Mean, Var, Std, Median, Mode, Skew, Kurtosis


def _var(seq):
    if len(seq) <= 1:
        return float("nan")
    else:
        return variance(seq)


def _std(seq):
    if len(seq) <= 1:
        return float("nan")
    else:
        return stdev(seq)


def _mode(seq):
    counts = Counter(seq)
    table = counts.most_common()
    max_freq = table[0][1]
    vals = set()
    for val, count in table:
        if count != max_freq:
            break
        vals.add(val)
    return vals


def _skew(seq):
    """Unbiased skewness"""
    if len(seq) <= 2:
        return float("nan")

    N = len(seq)

    # compute moments
    A = sum(seq) / N
    B = sum(n * n for n in seq) / N - A * A
    C = sum(n * n * n for n in seq) / N - A * A * A - 3 * A * B

    if B <= 1e-14:
        return float("nan")

    R = sqrt(B)
    return (sqrt(N * (N - 1)) * C) / ((N - 2) * R * R * R)


def _kurtosis(seq):
    if len(seq) <= 3:
        return float("nan")

    N = len(seq)

    # compute moments
    A = sum(seq) / N
    R = A * A

    B = sum(n ** 2 for n in seq) / N - R
    R *= A

    C = sum(n ** 3 for n in seq) / N - R - 3 * A * B
    R *= A

    D = sum(n ** 4 for n in seq) / N - R - 6 * B * A * A - 4 * C * A

    if B <= 1e-14:
        return float("nan")

    K = (N * N - 1) * D / (B * B) - 3 * ((N - 1) ** 2)
    return K / ((N - 2) * (N - 3))


@pytest.mark.parametrize("array", [[3, 0, 1, 7, 2], [3, -8, 1, 7, -2], [1], []])
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_mean(array, window_size, window_type):
    got = Mean(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=_mean, window_type=window_type)
    assert pytest.approx(list(got)) == list(expected)


# fmt: off
ARRAYS_TO_TEST_VAR = [
    [82, 80, 14, 73, 9, 19, 60, 31, 4, 87, 38, 36, 38, 58, 20, 97, 25, 99, 79, 31, 97, 73, 79, 71, 78, 56, 73, 24, 53, 59],
    [138, 136, 137, 137, 135, 136, 135, 135, 135],
    [8, 6, 7, 5, 3, 0, 9, -3, -1, -4, -1],
    [3, 5, 1, 4, 1],
    [5],
    [],
]
# fmt: on


@pytest.mark.parametrize("array", ARRAYS_TO_TEST_VAR)
@pytest.mark.parametrize("window_size", [3, 7, 10, 20])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_var(array, window_size, window_type):
    got = Var(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=_var, window_type=window_type)
    assert pytest.approx(list(got), nan_ok=True) == list(expected)


@pytest.mark.parametrize(
    "array", [[82, 80, 14, 73, 9, 19, 60, 31, 4, 87, 38, 36, 38, 58, 20]]
)
@pytest.mark.parametrize(
    "ddof,expected",
    [
        (
            0,
            [
                0.0,
                1.0,
                998.22222222222217,
                787.1875,
                1083.4400000000001,
                1050.4722222222224,
                854.91666666666663,
                575.88888888888903,
                657.55555555555566,
                873.0,
                738.47222222222229,
                660.55555555555554,
                600.66666666666663,
                629.91666666666663,
                454.80555555555549,
                145.59999999999999,
                182.0,
                240.88888888888891,
                361.0,
                0.0,
            ],
        ),
        (
            2,
            [
                float("nan"),
                float("nan"),
                2994.6666666666665,
                1574.375,
                1805.7333333333336,
                1575.7083333333335,
                1282.375,
                863.83333333333348,
                986.33333333333348,
                1309.5,
                1107.7083333333335,
                990.83333333333337,
                901.0,
                944.875,
                682.20833333333326,
                242.66666666666666,
                364.0,
                722.66666666666674,
                float("nan"),
                float("nan"),
            ],
        ),
        (
            4,
            [
                float("nan"),
                float("nan"),
                float("nan"),
                float("nan"),
                5417.2000000000007,
                3151.416666666667,
                2564.75,
                1727.666666666667,
                1972.666666666667,
                2619.0,
                2215.416666666667,
                1981.6666666666667,
                1802.0,
                1889.75,
                1364.4166666666665,
                728.0,
                float("nan"),
                float("nan"),
                float("nan"),
                float("nan"),
            ],
        ),
    ],
)
def test_rolling_var_variable_with_ddof(array, ddof, expected):
    r = Var(array, 6, ddof=ddof, window_type="variable")
    # Note: using an absolute tolerance of 1e-11 here rather than 1e-12
    # because for ddof=0 testcase, Var comutes the last value as
    # 5.229594535194337e-12 and not 0.0 (as np.var and statistics.pvariance give)
    assert pytest.approx(list(r), nan_ok=True, abs=1e-11) == expected


@pytest.mark.parametrize("array", ARRAYS_TO_TEST_VAR)
@pytest.mark.parametrize("window_size", [3, 7, 10, 20])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_std(array, window_size, window_type):
    got = Std(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=_std, window_type=window_type)
    assert pytest.approx(list(got), nan_ok=True) == list(expected)


@pytest.mark.parametrize(
    "array", [[3, 0, 1, 7, 2], [3, -8, 1, 7, -2, 8, 1, -7, -2, 9, 3], [1], []]
)
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_median(array, window_size, window_type):
    got = Median(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=_median, window_type=window_type)
    assert pytest.approx(list(got)) == list(expected)


@pytest.mark.parametrize("array", ["aasbbdasbfiuhf", "xxyxz", "x", ""])
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_mode(array, window_size, window_type):
    got = Mode(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=_mode, window_type=window_type)
    # NOTE: we copy the returned set so that it is not mutated after further iteration
    assert [set_.copy() for set_ in got] == list(expected)


@pytest.mark.parametrize(
    "array",
    [
        [3, -8, 1, 7, -2, 8, 1, -7, -2, 9, 3],
        [3.2, -8.1, 4.2, 7.7, -2.1, 0, 0, -2.1, -2.9, 2.4, 3.6],
        [3, 0, 1, 7, 2],
        [1],
        [],
    ],
)
@pytest.mark.parametrize("window_size", [3, 4, 5, 6])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_skew(array, window_size, window_type):
    got = Skew(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=_skew, window_type=window_type)
    assert pytest.approx(list(got), nan_ok=True) == list(expected)


@pytest.mark.parametrize(
    "array",
    [
        [3, -8, 1, 7, -2, 8, 1, -7, -2, 9, 3],
        [3.2, -8.1, 4.2, 7.7, -2.1, 0, 0, -2.1, -2.9, 2.4, 3.6],
        [3, 0, 1, 7, 2],
        [1],
        [],
    ],
)
@pytest.mark.parametrize("window_size", [4, 5, 6])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
def test_rolling_kurtosis(array, window_size, window_type):
    got = Kurtosis(array, window_size, window_type=window_type)
    expected = Apply(array, window_size, operation=_kurtosis, window_type=window_type)
    assert pytest.approx(list(got), nan_ok=True) == list(expected)
