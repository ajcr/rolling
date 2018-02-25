# rolling

![travis-ci](https://travis-ci.org/ajcr/rolling.svg?branch=master)

A collection of computationally efficient rolling window iterators for Python, with a simple iterface (a.k.a. 'sliding window', 'moving window').

Useful arithmetical, logical and statistical functions are implemented. There's also a more general 'apply' mode. Both fixed-length and variable-length windows are supported.

To get started, see the [Quickstart](https://github.com/ajcr/rolling#quickstart) section below, or have a look at the some [Recipes](https://github.com/ajcr/rolling/blob/master/doc/recipes.md).

## Overview

Naively applying builtin Python's functions to a window (e.g. `sum()` and `max()`) becomes increasingly slow as the window gets larger. The complexity is typically **O(k)** where **k** is the size of the window.

Luckily, for many operations there are algorithms that update a window in sublinear time (e.g. **O(log k)**) or constant time (**O(1)**). The rolling window algorithms implemented so far in this module are summarised below:

| Operation        | Update   | Memory | Comments |
| ---------------- |:--------:|:------:|-----------------------------|
| Sum              | O(1)     | O(k)   | Sum of window values |
| Mean             | O(1)     | O(k)   | Arithmetic mean of window values |
| Median           | O(log k) | O(k)   | Median, uses indexable skiplist (proposed by R. Hettinger) |
| Var              | O(1)     | O(k)   | Variance, uses Welford's algorithm for better numerical stability |
| Std              | O(1)     | O(k)   | Standard deviation, uses Welford's algorithm |
| Any              | O(1)     | O(1)   | True if *any* value in the window is True, else False |
| All              | O(1)     | O(1)   | True if *all* values in the window are True, else False |
| Min              | O(1)     | O(k)   | Minimum value, tracks ascending minima using a deque |
| MinHeap          | O(1)     | O(k)   | Minimum value, tracks ascending minima using a heap |
| Max              | O(1)     | O(k)   | Maximum value, tracks descending maxima using a deque |

See the References section below for more details about the algorithms and links to other resources.

## Installation

There are no external library dependencies for running this module.

The module is tested with Python 3.5 and above and Python 3.4 is also known to work. Python 2 is not currently supported.

```
git clone https://github.com/ajcr/rolling.git
cd rolling/
pip install .
```
If you want to run the tests you'll need to install [pytest](https://docs.pytest.org/en/latest/); once done, just run `pytest` from the base directory.

## Quickstart

Import the `rolling()` function:
```python
>>> from rolling import rolling
```
Now suppose we have this list:
```python
>>> counts = [1, 5, 2, 0, 3]
```
The `rolling()` function creates an [iterator object](https://docs.python.org/3/library/stdtypes.html#iterator-types) over this list, with a reduction operation for a given window size:
```python
>>> r_sum = rolling(counts, window_size=3, operation='Sum') # rolling sum
>>> r_all = rolling(counts, window_size=3, operation='All') # rolling all
>>> r_max = rolling(counts, window_size=3, operation='Max') # rolling max
```
The result of iterating over each rolling object using `list()` is shown below. Note that the window type is fixed by default, meaning that only windows of the specified size (3) are used:
```python
>>> list(r_sum)
[8, 7, 5]

>>> list(r_all)
[True, False, False]

>>> list(r_max)
[5, 5, 3]
```
As well as the built-in efficient algorithms provided by this module, any callable Python object can be applied to the rolling window. For instance, Python's `tuple()` function:
```python
>>> r_list = rolling(counts, window_size=3, operation=tuple)
>>> list(r_list)
[(1, 5, 2), (5, 2, 0), (2, 0, 3)]
```

Variable-length windows can be specified using the `window_type` argument. This allows windows smaller than the specified size to be evaluated at the beginning and end of the iterable. For instance:
```python
>>> r_list = rolling(counts, window_size=3, operation=list, window_type='variable')
>>> list(r_list)
[[1],
 [1, 5],
 [1, 5, 2],
 [5, 2, 0],
 [2, 0, 3],
 [0, 3],
 [3]]
```
## References and resources

Some rolling algorithms are widely known (e.g. 'Sum' and 'Mean') and I am not sure which source to cite.

Other rolling algorithms are very cleverly designed and I learned a lot by reading about them and seeing other peoples' implementations. Here are the main resources that I used:

- **Max** and **Min** are implemented using the Ascending Minima and Descending Maxima algorithms described by Richard Harter [here](http://www.richardhartersworld.com/cri/2001/slidingmin.html). This algorithm is also used in [pandas](http://pandas.pydata.org/) and [bottleneck](https://github.com/kwgoodman/bottleneck). My attention was first drawn to this algorithm by Jaime Fernandez del Rio's excellent talk ['The Secret Life Of Rolling Pandas'](https://www.youtube.com/watch?v=XM_r5La-1tA). The algorithm is also described by Keegan Carruthers-Smith [here](https://people.cs.uct.ac.za/~ksmith/articles/sliding_window_minimum.html), along with code examples.

- **Median** uses the indexable skiplist approach presented by Raymond Hettinger [here](http://code.activestate.com/recipes/577073/).

- **Var** and **Std** use [Welford's algorithm](https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#On-line_algorithm). I referred to the rolling variance implementation in [pandas](https://github.com/pandas-dev/pandas/blob/master/pandas/_libs/window.pyx#L635-L784) as well as an older edit of the Wikipedia page [Algorithms for calculating variance](https://en.wikipedia.org/w/index.php?title=Algorithms_for_calculating_variance&oldid=617145179).


## Discussion and future work

The algorithms implemented by this module are chosen to be efficient in the sense that the cost of computing each new return value scales efficiently with the size of window.

In practice you might find that it is quicker *not* to use the the 'efficient' algorithm, and instead apply a function to the window. This is especially true for very small window sizes where the cost of updating a window is relatively complex. For instance, while the window size `k` is less than approximately 50, it may quicker to use `rolling(array, k, min)` (apply Python's builtin minimum function) rather than using `rolling(array, k, 'Min')`.

With this in mind, in future it might be worth implementing some of the algorithms here in compiled code (e.g. as a C extension module, or using Cython) to improve speed.
