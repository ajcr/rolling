# rolling

A collection of efficient rolling/sliding window algorithms.

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

## Installation

Clone this repo, change into the new directory, and then type `python setup.py install`.

## Overview of the Algorithms

### Algorithm complexity

The *rolling* module implements efficient ways of updating a rolling window for a number of common operations.

Suppose the size of the window is **k**. Then the update time and overall space complexity for each algorithm is as follows:

| Operation                | Time     | Space |
| ------------------------ |:--------:|:-----:|
| Sum                      | O(1)     | O(k)  |
| Mean*                     | O(1)     | O(k)  |
| Median*                   | O(log k) | O(k)  |
| Var (Variance)*           | O(1)     | O(k)     |
| Std (Standard Deviation)* | O(1)     | O(k)     |
| Any                      | O(1)     | O(1)  |
| All                      | O(1)     | O(1)  |
| Min                      | O(1)     | O(k)  |
| Max                      | O(1)     | O(k)  |

* not yet implemented

### References and resources

Some rolling algorithms are relatively easy to discover. 

After some thought, **Sum** can be computed by keeping track of the two values entering and leaving the window in each iteration, and adding and subtracting these values from the total. **All** just requires tracking whether the count of consecutive 'true' values is greater-than-or-equal-to the size of the window.

However, other rolling algorithms are ingenious. I learned a lot by reading about them. Here are the resources that I used.

- **Max** and **Min** are implemented using the Ascending Maxima algorithm described by Richard Harter [here](http://www.richardhartersworld.com/cri/2001/slidingmin.html). This algorithm is used in *pandas* and *bottleneck* and I refferred to each implementation when writing mine. My attention was first drawn to this algorithm by Jaime Fernandez del Rio's excellent talk ['The Secret Life Of Rolling Pandas'](https://www.youtube.com/watch?v=XM_r5La-1tA).

- **Median** uses the indexable skiplist presented by Raymond Hettinger (cf. [here](http://code.activestate.com/recipes/577073/)).

- **Var** and **Std** use [Welford's algorithm](https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#On-line_algorithm). 

## Discussion and Future Work

The algorithms implemented in this module are chosen to be efficient in the sense that the cost of computing each new return value scales well with the size of window.

In practice you might find that it is quicker *not* to use the supplied efficient algorithm, and instead apply a function to the window. This is especially true for small window sizes.

With this in mind, it might be worth implementing some of the core algorithms in compiled code (e.g. as a C extension module, or using Cython) to improve speed.

Other work which would extend the usefulness of this module includes:

- Allowing operations on variable-length windows.
- Alternative algorithms that trade time complexity for a reduced memory footprint.
- Additional reduction operations for windows (e.g. longest increasing sequence), and weighted window algorithms.

