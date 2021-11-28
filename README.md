# rolling

![PyPI version](https://badge.fury.io/py/rolling.svg) ![travis-ci](https://travis-ci.org/ajcr/rolling.svg?branch=master) [![codecov](https://codecov.io/gh/ajcr/rolling/branch/master/graph/badge.svg)](https://codecov.io/gh/ajcr/rolling)

A collection of computationally efficient rolling window iterators for Python.

This module implements useful arithmetical, logical and statistical functions on rolling/moving/sliding windows (Sum, Min, Max, Median, Standard Deviation and more). There's also a flexible 'Apply' iterator whereby any function can be applied to the window. Both fixed-length and variable-length window iteration is supported.

To get started, see the [Overview](https://github.com/ajcr/rolling#overview) section below, or have a look at the some [recipes](https://github.com/ajcr/rolling/blob/master/doc/recipes.md).

## Installation

You can install the module using pip:
```
pip install rolling
```

Alternatively, you can install from source on GitHub if you want the very latest development changes:
```
git clone https://github.com/ajcr/rolling.git
cd rolling/
pip install .
```

There are no external library dependencies for running this module. If you want to run the tests you'll need to install [pytest](https://docs.pytest.org/en/latest/). Once done, just run `pytest` from the base directory.

## Overview

Here's a sequence of integers:
```python
seq = [3, 1, 4, 1, 5, 9, 2]
```
Suppose we want to find the **maximum** in each window of 5 consecutive integers:

![alt tag](https://github.com/ajcr/rolling/blob/master/assets/readme_example_1.png)

One way to do this would be to use Python's `max()` function and apply it to each consecutive slice of 5 elements:

```python
>>> [max(seq[i:i+5]) for i in range(len(seq) - (5-1))]
[5, 9, 9]
```

However, as well as being quite verbose, applying builtin functions (like `max()` and `sum()`) to a window becomes increasingly slow as the window size gets bigger. This is because all values in the window are visited each time the function is invoked, and so the complexity is typically _linear_ (i.e. **O(k)** where **k** is the size of the window).

It's clear by looking at the picture above that most of the values remain in the window when it is rolled forward. By keeping track of some information about the window and the values that are removed and added, an operation such as finding the maximum value can be completed much more efficiently, often in _constant_ time (i.e. **O(1)**, not dependent on the size of the window).

This library implements efficient ways to operate on windows:

```python
>>> import rolling              # import library
>>> roll = rolling.Max(seq, 5)  # iterator returning maximum of each window of size 5
>>> list(roll)
[5, 9, 9] 
```
Some of the other operations available are `Sum`, `Median`, `Std` (standard deviation), `Any`/`All` and `Entropy`. See below for a summary of the complexity of these operations.

As well as these efficient algorithms, any callable Python object can be applied to a window using the `Apply()` class. For example:
```python
>>> roll_tuple = rolling.Apply(seq, 5, operation=tuple)
>>> list(roll_tuple)
[(3, 1, 4, 1, 5),
 (1, 4, 1, 5, 9),
 (4, 1, 5, 9, 2)]
```

Variable-length windows can be specified using the `window_type` argument. This allows windows smaller than the specified size to be evaluated at the beginning and end of the iterable. For instance:
```python
>>> roll_list = rolling.Apply(seq, 3, operation=list, window_type='variable')
>>> list(roll_list)
[[3],
 [3, 1],
 [3, 1, 4],
 [1, 4, 1],
 [4, 1, 5],
 [1, 5, 9],
 [5, 9, 2],
 [9, 2],
 [2]]
```

Most of the methods implemented in this module support both fixed and variable size windows.

## Algorithmic Complexity

The algorithms implemented so far in this module are summarised below:

| Operation        | Update   | Memory | Comments |
| ---------------- |:--------:|:------:|-----------------------------|
| Sum              | O(1)     | O(k)   | Sum of window values |
| Product          | O(1)     | O(k)   | Product of window values |
| Nunique          | O(1)     | O(k)   | Number of unique window values |
| Mean             | O(1)     | O(k)   | Arithmetic mean of window values |
| Median           | O(log k) | O(k)   | Median, uses an indexable skiplist to maintain sorted order |
| Mode             | O(1)     | O(k)   | Set of most common values, tracked using a bi-directional counter |
| Var              | O(1)     | O(k)   | Variance, uses Welford's algorithm for better numerical stability |
| Std              | O(1)     | O(k)   | Standard deviation, uses Welford's algorithm |
| Skew             | O(1)     | O(k)   | Skewness of the window |
| Kurtosis         | O(1)     | O(k)   | Kurtosis of the window |
| Any              | O(1)     | O(1)   | True if *any* value in the window is True, else False |
| All              | O(1)     | O(1)   | True if *all* values in the window are True, else False |
| Min              | O(1)     | O(k)   | Minimum value, tracks ascending minima using a deque |
| MinHeap          | O(1)     | O(k)   | Minimum value, tracks ascending minima using a heap |
| Max              | O(1)     | O(k)   | Maximum value, tracks descending maxima using a deque |
| Entropy          | O(1)     | O(k)   | Shannon entropy of the window (fixed-size windows only) |
| PolynomialHash   | O(1)     | O(k)   | Hash of rolling window |
| Match            | O(k)     | O(k)   | True if window matches a target sequence (linear update in worst case) |

See the [References](https://github.com/ajcr/rolling#references-and-resources) section below for more details about the algorithms and links to other resources.

## References and resources

Some rolling algorithms are widely known (e.g. `Sum`) and so I am not sure which source to cite. Some algorithms I made up as I was putting the module together (e.g. `Any`, `All`), but these are relatively simple and probably exist elsewhere.

Other rolling algorithms are very cleverly designed and I learned a lot by reading about them and seeing other peoples' implementations. Here are the main resources that I used:

- `Max` and `Min` are implemented using the Ascending Minima and Descending Maxima algorithms described by Richard Harter [here](http://www.richardhartersworld.com/cri/2001/slidingmin.html). This algorithm is also used in [pandas](http://pandas.pydata.org/) and [bottleneck](https://github.com/kwgoodman/bottleneck). My attention was first drawn to this algorithm by Jaime Fernandez del Rio's excellent talk _[The Secret Life Of Rolling Pandas](https://www.youtube.com/watch?v=XM_r5La-1tA)_. The algorithm is also described by Keegan Carruthers-Smith [here](https://people.cs.uct.ac.za/~ksmith/articles/sliding_window_minimum.html), along with code examples.

- `Median` uses the indexable skiplist approach presented by Raymond Hettinger [here](http://code.activestate.com/recipes/577073/).

- `Var` and `Std` use [Welford's algorithm](https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#On-line_algorithm). I referred to the rolling variance implementation in [pandas](https://github.com/pandas-dev/pandas/blob/master/pandas/_libs/window.pyx#L635-L784) as well as an older edit of the Wikipedia page [Algorithms for calculating variance](https://en.wikipedia.org/w/index.php?title=Algorithms_for_calculating_variance&oldid=617145179).

## Discussion and future work

The algorithms implemented by this module are chosen to be efficient in the sense that the cost of computing each new return value scales efficiently with the size of window.

In practice you might find that it is quicker *not* to use the the 'efficient' algorithm, and instead apply a function to the window. This is especially true for very small window sizes where the cost of updating a window is relatively complex. For instance, while the window size `k` is less than approximately 50, it may quicker to use `rolling.Apply(array, k, min)` (apply Python's builtin minimum function `min()`) rather than using `rolling.Min(array, k)`.

With this in mind, it might be worth implementing some of the algorithms here in compiled code (e.g. as a C extension module, or using Cython) to improve speed.
