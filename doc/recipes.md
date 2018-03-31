# Recipes

Here are a few applications of the rolling module, demonstrating how rolling iterators can by combined with Python's standard library to solve everyday problems in very few lines of code.

## Consecutive Heads

Flipping an unbiased coin 1 million times, check to see if there is a run of consecutive 25 heads.

```python
# Setup: 1 million coin flips of an unbiased coin

import random

coin_flips = (random.choice('HT') for _ in range(10**6))

# Solution

import rolling

is_heads = (flip == 'H' for flip in coin_flips)

any(rolling.All(is_heads, 25))
```

## Peak-to-Peak

In a stream of auction bids, find the greatest difference between the maximum and minimum bids occurring in a window of size 500.

```python
# Setup: 1 million random integers between 100 and 10000

import random

bids = (random.randint(100, 10000) for _ in range(10**6))

# Solution

import itertools
import rolling

bids_1, bids_2 = itertools.tee(bids)

size = 500

roll_max = rolling.Max(bids_1, size)
roll_min = rolling.Min(bids_2, size)

max(hi-lo for hi, lo in zip(roll_max, roll_min))
```

## Ngrams

Count up all substrings with two letters (bigrams) in a sentence and return the five most common.

```python
# Setup

sentence = """As a hungry mosquito flies over a steamy swamp a
greedy dragonfly hovers just behind her and behind the dragonfly
waits a famished frog"""

# Solution

from collections import Counter
import rolling

bigrams = rolling.rolling(sentence, 2, operation=tuple)

bigrams_no_spaces = (bigram for bigram in bigrams if ' ' not in bigram)
bigram_freqs = Counter(bigrams_no_spaces)
bigram_freqs.most_common(5)
```

## Too Many Requests

Track incoming requests to a website. If one or more users is responsible for more than a quarter of the last 1000 requests, print a warning message:

```python
# Setup

USER_IP_ADDRESSES = (...) # some infinite stream of IP addresses of website users
WINDOW_SIZE = 1000

# Solution

import rolling

for ip_addresses, count in rolling.Mode(USER_IP_ADDRESSES, WINDOW_SIZE, return_count=True):
    if count > WINDOW_SIZE / 4:
        print('Warning: {} requests each from IP addresses {}.format(count, ', '.join(ip_addresses)))
```
