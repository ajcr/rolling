# rolling

![PyPI version](https://img.shields.io/pypi/v/rolling.svg?color=brightgreen)

A collection of computationally efficient rolling window iterators for Python.

Useful arithmetical, logical and statistical operations on rolling windows (including `Sum`, `Min`, `Max`, `Mean`, `Median` and more). Both fixed-length and variable-length windows are supported for most operations. Many operations also support "indexed" windows.

To get started, see the [Overview](https://github.com/ajcr/rolling#overview) section below, or have a look at the some [recipes](https://github.com/ajcr/rolling/blob/master/doc/recipes.md).

## Installation

```
pip install rolling
```

You can also install from source if you want the very latest development changes:
```
git clone https://github.com/ajcr/rolling.git
cd rolling/
pip install .
```

There are no external library dependencies for running this module. If you want to run the unit tests, you'll need to install [pytest](https://docs.pytest.org/en/latest/). Once done, just run `pytest` from the base directory.

## Overview

Consider a sequence of integers:
```python
seq = [3, 1, 4, 1, 5, 9, 2]
```
Suppose we want to find the **maximum** value in each window of five consecutive integers:

![alt tag](https://github.com/ajcr/rolling/blob/master/assets/readme_example_1.png)

One way to do this would be to use Python's `max` function and apply it to each consecutive slice of five elements:

```python
>>> [max(seq[i:i+5]) for i in range(len(seq) - (5-1))]
[5, 9, 9]
```

However, as well as being quite verbose, applying builtin functions (like `max` and `sum`) to a window becomes increasingly slow as the window size gets bigger. This is because all values in the window are visited each time the function is invoked, and so the complexity is typically _linear_ (i.e. **O(k)** where **k** is the size of the window).

It's clear by looking at the picture above that most of the values remain in the window when it is rolled forward. By keeping track of information about the window and the values that are removed and added, an operation such as finding the maximum value can be completed much more efficiently, often in _constant_ time (i.e. **O(1)**, not dependent on the size of the window).

This library implements efficient ways to perform useful operations on rolling windows:

```python
>>> import rolling              # import library
>>> roll = rolling.Max(seq, 5)  # iterator returning maximum of each window of size 5
>>> list(roll)
[5, 9, 9] 
```

Note that these time complexity values apply to "fixed" and "variable" window types (not the "indexed" window type which depends on the index values encountered).

## Operations

The algorithms implemented so far in this module are summarised below. 

The cost of updating the window (rolling it forward) and the memory footprint of the `rolling` object are given, where `k` denotes the size of the window.

The 'Builtin' column shows the comparable method that is found in the Python standard library. This method could be applied to the window (at higher computational cost) to get the same result. Note that it may not be equivalent in all cases, for example due to differences in floating point arithmetic.


### Arithmetical

Rolling objects to apply common aggregation or measurement operations to the window.

| Object           | Update   | Memory | Description                            | Builtin |
| ---------------- |:--------:|:------:|----------------------------------------|----------------|
| `Sum`            | O(1)     | O(k)   | Sum of the window values               | [`sum`](https://docs.python.org/3/library/functions.html#sum)  |
| `Product`        | O(1)     | O(k)   | Product of the window values           | [`math.prod`](https://docs.python.org/3.9/library/math.html#math.prod) |
| `Nunique`        | O(1)     | O(k)   | Number of unique window values         | N/A |
| `Min`            | O(1)     | O(k)   | Minimum value of window                | [`min`](https://docs.python.org/3/library/functions.html#min) |
| `MinHeap`        | O(log(k))| O(k)   | Minimum value (internally uses a heap) | [`min`](https://docs.python.org/3/library/functions.html#min) |
| `Max`            | O(1)     | O(k)   | Maximum value of window                | [`max`](https://docs.python.org/3/library/functions.html#max) |

### Statistical

Rolling objects to apply statistical operations to the window.

| Object           | Update   | Memory | Description                                                     | Builtin |
| ---------------- |:--------:|:------:|-----------------------------------------------------------------|----------------------|
| `Mean`           | O(1)     | O(k)   | Arithmetic mean of window values                                | [`statistics.mean`](https://docs.python.org/3.9/library/statistics.html#statistics.mean) |
| `Median`         | O(log k) | O(k)   | Median value of window: O(log k) update if 'skiplist' used      | [`statistics.median`](https://docs.python.org/3.9/library/statistics.html#statistics.median) |
| `Mode`           | O(1)     | O(k)   | Set of most frequently appearing values in window               | [`statistics.multimode`](https://docs.python.org/3.9/library/statistics.html#statistics.multimode) |
| `Var`            | O(1)     | O(k)   | Variance of window, with specified degrees of freedom           | [`statistics.pvariance`](https://docs.python.org/3.9/library/statistics.html#statistics.pvariance) |
| `Std`            | O(1)     | O(k)   | Standard deviation of window, with specified degrees of freedom | [`statistics.pstdev`](https://docs.python.org/3.9/library/statistics.html#statistics.pstdev) |
| `Skew`           | O(1)     | O(k)   | Skewness of the window                                          | N/A |
| `Kurtosis`       | O(1)     | O(k)   | Kurtosis of the window                                          | N/A |

### Logical

Rolling objects to apply a logical operation to the window.

| Object           | Update   | Memory | Description                                                                              | Builtin |
| ---------------- |:--------:|:------:|------------------------------------------------------------------------------------------|---------|
| `Any`            | O(1)     | O(1)   | True if *any* value in the window is True in a Boolean context, else False               | [`any`](https://docs.python.org/3/library/functions.html#any) |
| `All`            | O(1)     | O(1)   | True if *all* values in the window are True in a Boolean context, else False             | [`all`](https://docs.python.org/3/library/functions.html#all) |
| `Monotonic`      | O(1)     | O(1)   | True if *all* values in the window are monotonic increasing or decreasing                | N/A     |
| `Match`          | O(k)     | O(k)   | True if window is equal to a specified target sequence (O(k) update if match, else O(1)) | N/A     |

### Miscellaneous

Rolling objects implementing other operations.

| Object           | Update   | Memory | Description                                                                                             | Builtin |
| ---------------- |:--------:|:------:|---------------------------------------------------------------------------------------------------------|---------|
| `Apply`          | ?        | O(k)   | Applies a specified callable object to the window (thus update complexity is dependent on the callable) | N/A |
| `Entropy`        | O(1)     | O(k)   | Shannon entropy of the window (fixed-size windows only)                                                 | N/A |
| `JaccardIndex`   | O(1)     | O(k+s) | Jaccard index (similarity coefficient) of window with a target set (s is size of target set)            | N/A |
| `PolynomialHash` | O(1)     | O(k)   | [Polynomial hash](https://en.wikipedia.org/wiki/Rolling_hash#Polynomial_rolling_hash) of window         | N/A |


By default, fixed length windows are used in all operations. Variable-length windows can be specified using the `window_type` argument.

This allows windows smaller than the specified size to be evaluated at the beginning and end of the iterable. For instance, here's the `Apply` operation being used to apply Python's `tuple` callable to variable-length windows:
```python
>>> seq = [3, 1, 4, 1, 5, 9, 2]
>>> roll_list = rolling.Apply(seq, 3, operation=tuple, window_type='variable')
>>> list(roll_list)
[(3,),
 (3, 1),
 (3, 1, 4),
 (1, 4, 1),
 (4, 1, 5),
 (1, 5, 9),
 (5, 9, 2),
 (9, 2),
 (2,)]
```

If values are indexed by a monotoncally-increasing index (e.g. with an integer key, timestamp or datetime) then the indexed window type can be used. The size of the window is the maximum distance between the oldest and newest values (e.g. an integer, or timedelta):
```python
>>> idx = [0, 1, 2, 6, 7, 11, 15]
>>> seq = [3, 1, 4, 1, 5,  9,  2]
>>> roll_list_idx = rolling.Apply(zip(idx, seq), window_size=3, operation=tuple, window_type='indexed')
>>> list(roll_list_idx)
[(3,),
 (3, 1),
 (3, 1, 4),
 (1,),
 (1, 5),
 (9,),
 (2,)]
```

## References and resources

Some rolling algorithms are widely known (e.g. `Sum`), so I am not sure which source to cite. Some algorithms I made up as I was putting the module together (e.g. `Any`, `All`), but these are relatively simple and probably exist elsewhere.

Other rolling algorithms are very cleverly designed by others and I learned a lot by reading their implementations. Here are the main resources that I used:

- `Max` and `Min` are implemented using the Ascending Minima and Descending Maxima algorithms described by Richard Harter [here](http://www.richardhartersworld.com/cri/2001/slidingmin.html). This algorithm is also used in [pandas](http://pandas.pydata.org/) and [bottleneck](https://github.com/kwgoodman/bottleneck). My attention was first drawn to this algorithm by Jaime Fernandez del Rio's excellent talk _[The Secret Life Of Rolling Pandas](https://www.youtube.com/watch?v=XM_r5La-1tA)_. The algorithm is also described by Keegan Carruthers-Smith [here](https://people.cs.uct.ac.za/~ksmith/articles/sliding_window_minimum.html), along with code examples.

- `Median` uses the indexable skiplist approach presented by Raymond Hettinger [here](http://code.activestate.com/recipes/577073/).

- `Var` and `Std` use [Welford's algorithm](https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#On-line_algorithm). I referred to the rolling variance implementation in [pandas](https://github.com/pandas-dev/pandas/blob/master/pandas/_libs/window.pyx#L635-L784) as well as an older edit of the Wikipedia page [Algorithms for calculating variance](https://en.wikipedia.org/w/index.php?title=Algorithms_for_calculating_variance&oldid=617145179).

## Discussion and future work

The algorithms implemented by this module are chosen to be efficient in the sense that the cost of computing each new window value scales efficiently with the size of window.

In practice you might find that it is quicker *not* to use the the 'efficient' algorithm, and instead apply a function directly to the window. This is especially true for very small window sizes where the cost of updating a window is relatively complex. For instance, while the window size `k` is less than approximately 50, it may quicker to use `rolling.Apply(array, k, min)` (apply Python's builtin minimum function `min`) rather than using `rolling.Min(array, k)`.

With this in mind, it might be worth implementing some of the algorithms in this module in more specialised/compiled code to improve performance.
