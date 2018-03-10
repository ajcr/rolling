import pytest

from rolling.stats import Mean, Var, Std, Median, Mode

@pytest.mark.parametrize('array,window_size,expected', [
    ([3, 0, 1, 7, 2], 6, []),
    ([3, 0, 1, 7, 2], 5, [13/5]),
    ([3, 0, 1, 7, 2], 4, [11/4, 10/4]),
    ([3, 0, 1, 7, 2], 3, [4/3, 8/3, 10/3]),
    ([3, 0, 1, 7, 2], 2, [3/2, 1/2, 8/2, 9/2]),
    ([3, 0, 1, 7, 2], 1, [3, 0, 1, 7, 2]),

    ([3, -8, 1, 7, -2], 5, [1/5]),
    ([3, -8, 1, 7, -2], 4, [3/4, -2/4]),
    ([3, -8, 1, 7, -2], 3, [-4/3, 0/3, 6/3]),
    ([3, -8, 1, 7, -2], 2, [-5/2, -7/2, 8/2, 5/2]),
    ([3, -8, 1, 7, -2], 1, [3, -8, 1, 7, -2]),

    ([],  5, []),
    ([1], 5, []),
])
def test_rolling_mean(array, window_size, expected):
    r = Mean(array, window_size)
    assert pytest.approx(list(r)) == expected

@pytest.mark.parametrize('array', [
    [82, 80, 14, 73,  9, 19, 60, 31,  4, 87, 38, 36, 38, 58, 20,
     97, 25, 99, 79, 31, 97, 73, 79, 71, 78, 56, 73, 24, 53, 59]
])
@pytest.mark.parametrize('window_size,expected', [
    (100,
    []),
    (5,
    [1354.3, 1190.5, 860.5, 739.8, 498.3, 1106.7, 977.5, 900.7, 881.8000000000001,
     476.8, 182, 878.1999999999999, 978.3, 1429.7, 1499, 1281.2, 1281.2,
     753.2, 601.2, 585.2, 105.80000000000001, 85.3, 85.3, 481.29999999999995,
     450.70000000000005, 321.5]),
    (10,
    [1129.8777777777777, 970.5, 787.6555555555556, 722.0555555555555, 632.8888888888889,
     574.1, 834.1, 854.7111111111111, 1129.7333333333333, 922.2333333333333,
     871.2111111111111, 1034.4444444444443, 990.4555555555555, 942.6222222222223,
     936.9888888888889, 666.3222222222223, 614.8444444444444, 378.0444444444445,
     517.2111111111111, 510.27777777777777, 386.4555555555556]),
    (20,
    [958, 1021.3552631578947, 1001.5157894736842, 970.5552631578947,
     966.4710526315789, 888.2105263157895, 812.5552631578947, 823.9473684210526,
     846.6605263157895, 687.4105263157895, 648.8]),
])
def test_rolling_var(array, window_size, expected):
    r = Var(array, window_size)
    assert pytest.approx(list(r)) == expected

@pytest.mark.parametrize('array', [
    [82, 80, 14, 73,  9, 19, 60, 31,  4, 87, 38, 36, 38, 58, 20]
])
@pytest.mark.parametrize('window_size,expected', [
    (4,
    [float('nan'), 2, 1497.3333333333333, 1049.5833333333333,
     1420.6666666666667, 886.9166666666666, 963.5833333333334, 487.5833333333333,
     563.0, 1288.3333333333333, 1196.6666666666667, 1172.9166666666667,
     617.5833333333334, 107.66666666666667, 242.66666666666666, 361.3333333333333,
     722, float('nan')]),
    (7,
    [float('nan'), 2, 1497.3333333333333, 1049.5833333333333,
     1354.3, 1260.5666666666666, 1077.8095238095239, 873.8095238095239,
     707.3333333333334, 1079.2857142857142, 874.2857142857143, 740.5714285714286,
     663.6666666666666, 652.2380952380953, 708.8095238095237, 545.7666666666667,
     182, 242.66666666666666, 361.3333333333333, 722,
     float('nan')]),
    (11,
    [float('nan'), 2, 1497.3333333333333, 1049.5833333333333,
     1354.3, 1260.5666666666666, 1077.8095238095239, 960.5714285714286,
     1036.5, 1129.8777777777777, 1022.5636363636364, 876.2,
     708.9636363636364, 680.9636363636364, 599.0545454545455, 574.1,
     589.75, 618, 708.8095238095237, 545.7666666666667,
     182, 242.66666666666666, 361.3333333333333, 722,
     float('nan')]),
])
def test_rolling_var_variable(array, window_size, expected):
    r = Var(array, window_size, window_type='variable')
    assert pytest.approx(list(r), nan_ok=True) == expected

@pytest.mark.parametrize('array,window_type,expected', [
    ([],  'fixed', []),
    ([3], 'fixed', []),
    ([],  'variable', []),
    ([1], 'variable', [float('nan')]),
])
def test_rolling_var_over_short_iterable(array, window_type, expected):
    r = Var(array, 5, window_type=window_type)
    assert pytest.approx(list(r), nan_ok=True) == expected

@pytest.mark.parametrize('array', [
    [82, 80, 14, 73,  9, 19, 60, 31,  4, 87, 38, 36, 38, 58, 20]
])
@pytest.mark.parametrize('ddof,expected', [
    (0,
    [0.0, 1.0, 998.22222222222217, 787.1875,
     1083.4400000000001, 1050.4722222222224, 854.91666666666663, 575.88888888888903,
     657.55555555555566, 873.0, 738.47222222222229, 660.55555555555554,
     600.66666666666663, 629.91666666666663, 454.80555555555549, 145.59999999999999,
     182.0, 240.88888888888891, 361.0, 0.0]),
    (2,
    [float('nan'), float('nan'), 2994.6666666666665, 1574.375,
     1805.7333333333336, 1575.7083333333335, 1282.375, 863.83333333333348,
     986.33333333333348, 1309.5, 1107.7083333333335, 990.83333333333337,
     901.0, 944.875, 682.20833333333326, 242.66666666666666,
     364.0, 722.66666666666674, float('nan'), float('nan')]),
    (4,
    [float('nan'), float('nan'), float('nan'), float('nan'),
     5417.2000000000007, 3151.416666666667, 2564.75, 1727.666666666667,
     1972.666666666667, 2619.0, 2215.416666666667, 1981.6666666666667,
     1802.0, 1889.75, 1364.4166666666665, 728.0,
     float('nan'), float('nan'), float('nan'), float('nan')]),
])
def test_rolling_var_variable_with_ddof(array, ddof, expected):
    r = Var(array, 6, ddof=ddof, window_type='variable')
    # Note: using an absolute tolerance of 1e-11 here rather than 1e-12
    # because for ddof=0 testcase, Var comutes the last value as
    # 5.229594535194337e-12 and not 0.0 (as np.var and statistics.pvariance give)
    assert pytest.approx(list(r), nan_ok=True, abs=1e-11) == expected

@pytest.mark.parametrize('array', [
    [10, 49, 87, 39, 91, 57, 53, 46, 4, 57, 3, 99, 28, 61, 44, 31, 97, 70, 88, 59]
])
@pytest.mark.parametrize('window_size,expected', [
    (4,
    [31.80539786472311, 26.350205565295564, 24.839484696748443, 22.06052281036573,
     20.02290355234891, 24.426761280748348, 24.426761280748348, 28.077274321652617,
     46.30604712129939, 41.23408784003837, 41.61229786172993, 30.474032661705056,
     15.033296378372908, 28.605069480775605, 29.24038303442689, 29.24038303442689,
     17.175564037317667]),
    (7,
    [27.823422815010684, 20.43456455546407, 29.599710423293963, 25.947749695989327,
     31.389261129974283, 33.4457627752612, 33.58996448771142, 34.18019476664394,
     34.15510838178425, 30.432595307381476, 36.04824809163672, 29.148225462608313,
     27.002645373052935, 23.17839716714888]),
    (17,
    [30.44450109722318, 28.913410281695363, 30.02756086938641, 28.98085067561601]),
])
def test_rolling_std(array, window_size, expected):
    r = Std(array, window_size)
    assert pytest.approx(list(r)) == expected

@pytest.mark.parametrize('array,window_size,expected', [
    ([3, 0, 1, 7, 2], 6, []),
    ([3, 0, 1, 7, 2], 5, [2]),
    ([3, 0, 1, 7, 2], 4, [2.0, 1.5]),
    ([3, 0, 1, 7, 2], 3, [1, 1, 2]),
    ([3, 0, 1, 7, 2], 2, [1.5, 0.5, 4.0, 4.5]),
    ([3, -8, 1, 7, -2, 8, 1, -7, -2, 9, 3], 5, [1, 1, 1, 1, -2, 1, 1]),
    ([3, -8, 1, 7, -2, 8, 1, -7, -2, 9, 3], 8, [1.0, -0.5, 1.0, 2.0]),
    ([3, -8, 1, 7, -2, 8, 1, -7, -2, 9, 3], 9, [1, 1, 1]),
    ([],  5, []),
    ([1], 5, []),
])
def test_rolling_median(array, window_size, expected):
    r = Median(array, window_size)
    assert pytest.approx(list(r)) == expected

@pytest.mark.parametrize('array,window_size,expected', [
    ([3, 0, 1, 7, 2], 5, [3, 1.5, 1, 2.0, 2, 1.5, 2, 4.5, 2]),
    ([3, 0, 1, 7, 2], 4, [3, 1.5, 1, 2.0, 1.5, 2, 4.5, 2]),
    ([3, 0, 1, 7, 2], 3, [3, 1.5, 1, 1, 2, 4.5, 2]),
    ([3, 0, 1, 7, 2], 2, [3, 1.5, 0.5, 4.0, 4.5, 2]),
    ([3, 0, 1, 7, 2], 1, [3, 0, 1, 7, 2]),
    ([], 5, []),
])
def test_rolling_median_variable(array, window_size, expected):
    r = Median(array, window_size, window_type='variable')
    assert pytest.approx(list(r)) == expected


@pytest.mark.parametrize('array,window_size,expected', [
    ('xxyxz', 5, [{'x'}]),
    ('xxyxz', 4, [{'x'}, {'x'}]),
    ('xxyxz', 3, [{'x'}, {'x'}, {'x', 'y', 'z'}]),
    ('xxyxz', 2, [{'x'}, {'x', 'y'}, {'x', 'y'}, {'x', 'z'}]),
    ('xxyxz', 1, [{'x'}, {'x'}, {'y'}, {'x'}, {'z'}]),

    ([],  5, []),
    (['x'], 5, []),
])
def test_rolling_mode(array, window_size, expected):
    r = Mode(array, window_size)
    # NOTE: we copy the returned set so that it is not
    # mutated after further iteration
    assert [set_.copy() for set_ in (r)] == expected


@pytest.mark.parametrize('array,window_size,expected', [
    ('xxyxz', 5, [{'x'}, {'x'}, {'x'}, {'x'}, {'x'}, {'x'}, {'x', 'y', 'z'}, {'x', 'z'}, {'z'}]),
    ('xxyxz', 4, [{'x'}, {'x'}, {'x'}, {'x'}, {'x'}, {'x', 'y', 'z'}, {'x', 'z'}, {'z'}]),
    ('xxyxz', 3, [{'x'}, {'x'}, {'x'}, {'x'}, {'x', 'y', 'z'}, {'x', 'z'}, {'z'}]),
    ('xxyxz', 2, [{'x'}, {'x'}, {'x', 'y'}, {'x', 'y'}, {'x', 'z'}, {'z'}]),
    ('xxyxz', 1, [{'x'}, {'x'}, {'y'}, {'x'}, {'z'}]),

    ([],  5, []),
    (['x'], 5, [{'x'}]),
])
def test_rolling_mode_variable(array, window_size, expected):
    r = Mode(array, window_size, window_type='variable')
    # NOTE: we copy the returned set so that it is not
    # mutated after further iteration
    assert [set_.copy() for set_ in (r)] == expected
