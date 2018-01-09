# rolling

A collection of efficient rolling/sliding window algorithms for Python.

## Overview

This module provides implementations of useful rolling-window operations, including sum, mean, and max. These operations can be applied over any iterable Python object, finite or infinite (lists, generators, files, and so on). 

Suppose the size of the window is **k**. The time taken to apply a builtin Python function such as `sum()` to the window scales linearly as the size increases, that is **O(k)**, as the full window must be iterated over with each roll forward. This can be unacceptably slow for larger windows.

For many operations there exist algorithms that compute the new value for a window in constant time, **O(1)**. The rolling window algorithms implemented in this module are summarised below:

| Operation                | Update Time | Space Required | Comments |
| ------------------------ |:--------:|:-----:|-----------------------------|
| Sum                      | O(1)     | O(k)  | Sum of window values |
| Mean                     | O(1)     | O(k)  | Arithmetic mean of window |
| Median                   | O(log k) | O(k)  | Uses an indexable skiplist proposed by R. Hettinger |
| Var                      | O(1)     | O(k)  | Rolling variance, uses Welford's algorithm |
| Std                      | O(1)     | O(k)  | Rolling standard deviation, uses Welford's algorithm |
| Any                      | O(1)     | O(1)  | True if any value is true, else false |
| All                      | O(1)     | O(1)  | True if all values are true, else false |
| Count                    | O(1)     | O(k)  | Number of true values in the window |
| Min                      | O(1)     | O(k)  | Uses 'Ascending Minima' algorithm | 
| Max                      | O(1)     | O(k)  | Uses 'Descending Maxima' algorithm |

See the References section below for more details about the algorithms. 

## Installation

There are no library dependencies for running this module.

```
git clone https://github.com/ajcr/rolling.git
cd rolling/
pip install .
```
If you want to run the tests you'll need to install pytest; once done, just run `pytest` from the base directory.

## Quickstart

Import the `rolling()` function:
```python
>>> from rolling import rolling
```
Now suppose we have this list:
```python
>>> counts = [1, 5, 2, 0, 3]
```
The `rolling()` function creates an [iterator object](https://docs.python.org/3/library/stdtypes.html#iterator-types) over the list (or any other iterable) with a specified window size and reduction operation:
```python
>>> r_sum = rolling(counts, window_size=3, func='Sum') # rolling sum
>>> r_all = rolling(counts, window_size=3, func='All') # rolling all
>>> r_max = rolling(counts, window_size=3, func='Max') # rolling max
```
The result of iterating over each rolling object is shown below:
```python
>>> list(r_sum)
[8, 7, 5]
>>> list(r_all)
[True, False, False]
>>> list(r_max)
[5, 5, 3]
```
As well as the built-in efficient algorithms, any callable Python object can be applied to the rolling window when using the `rolling()` function:
```python
>>> r_list = rolling(counts, window_size=3, func=tuple)
>>> list(r_list)
[(1, 5, 2), (5, 2, 0), (2, 0, 3)]
```

## Discussion and future work

The algorithms implemented by this module are chosen to be efficient in the sense that the cost of computing each new return value scales well with the size of window.

In practice you might find that it is quicker *not* to use the the 'efficient' algorithm, and instead apply a function to the window. This is especially true for very small window sizes where the cost of updating a window is relatively complex. For instance, while the window size `k` is less than approximately 50, it may quicker to use `rolling(array, k, min)` (apply Python's builtin minimum function) rather than using `rolling(array, k, 'Min')`.

With this in mind, in future it might be worth implementing some of the algorithms here in compiled code (e.g. as a C extension module, or using Cython) to improve speed.

Other work which would extend the usefulness of this module includes:

- Allowing operations on variable-length windows.
- Alternative algorithms that trade time complexity for a reduced memory footprint.
- Additional reduction operations for windows (e.g. longest increasing subsequence), and weighted window algorithms.

## References and resources

Some rolling algorithms are widely known (e.g. 'Sum' and 'Mean') and I am not sure which source to cite. 

Other rolling algorithms are very cleverly designed and I learned a lot by reading about them and seeing other peoples' implementations. Here are the main resources that I used:

- **Max** and **Min** are implemented using the Ascending Minima and Descending Maxima algorithms described by Richard Harter [here](http://www.richardhartersworld.com/cri/2001/slidingmin.html). This algorithm is also used in [pandas](http://pandas.pydata.org/) and [bottleneck](https://github.com/kwgoodman/bottleneck). My attention was first drawn to this algorithm by Jaime Fernandez del Rio's excellent talk ['The Secret Life Of Rolling Pandas'](https://www.youtube.com/watch?v=XM_r5La-1tA). The algorithm is also described by Keegan Carruthers-Smith [here](https://people.cs.uct.ac.za/~ksmith/articles/sliding_window_minimum.html), along with code examples.

- **Median** uses the indexable skiplist approach presented by Raymond Hettinger [here](http://code.activestate.com/recipes/577073/).

- **Var** and **Std** use [Welford's algorithm](https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#On-line_algorithm). I referred to the rolling variance implementation in [pandas](https://github.com/pandas-dev/pandas/blob/master/pandas/_libs/window.pyx#L635-L784) as well as an older edit of the Wikipedia page [Algorithms for calculating variance](https://en.wikipedia.org/w/index.php?title=Algorithms_for_calculating_variance&oldid=617145179).

