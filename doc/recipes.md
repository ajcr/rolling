# Recipes

Here a few applications of the rolling module.

## consecutive heads

Flipping an unbiased coin 1 million times, do we observe a run of consecutive 25 heads?

```python
import random
import rolling

random.seed(36518)

# Setup: 1 million coin flips of an unbiased coin

coin_flips = (random.choice('HT') for _ in range(10**6))
is_heads = (flip == 'H' for flip in coin_flips)

# Solution

any(rolling.All(is_heads, 25))
```

## rolling range

In a stream of auction bids, we want to track the largest difference between the maximum and minimum values occurring in a window of size 75.

```python
import itertools
import random
import rolling

random.seed(36518)

# Setup: 1 million random integers between 100 and 10000

bids = (random.randint(100, 10000) for _ in range(10**6))

# Solution

bids_1, bids_2 = itertools.tee(bids)

size = 75

roll_max = rolling.Max(bids_1, size)
roll_min = rolling.Min(bids_2, size)

differences = (hi-lo for hi, lo in zip(roll_max, roll_min)) 
```
