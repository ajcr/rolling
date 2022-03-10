# Recipes

Here are a few applications of the rolling module, demonstrating how rolling iterators can by combined with Python's builtin functions to solve various problems in a few lines of code.

## Consecutive Heads

Flip a fair coin 1 million times. Is there is a run of consecutive 25 heads?

### Setup
Here are a million coin flips:
```python
import random

coin_flips = (random.choice('HT') for _ in range(1_000_000))
```

### Solution

Generate a stream of "is_heads" Boolean values. Use `rolling.All` to track whether all values in the current window are true (i.e. "heads"). Use Python's `any()` builtin to reduce this iterator until the first window of all heads is seen (or the stream of coin flips ends).

```python
import rolling

WINDOW_SIZE = 25

is_heads = (flip == 'H' for flip in coin_flips)

any(rolling.All(is_heads, WINDOW_SIZE))
```

## Peak-to-Trough

Consider a stream of auction bids. Find the largest difference between the maximum and minimum bids occurring in a window of size 500.

### Setup

Here are 1 million random integers between 100 and 10000 (the "bids"):
```python
import random

bids = (random.randint(100, 10000) for _ in range(10**6))
```

### Solution

Keep track of the maximum and minimum values in the window. The stream is duplicated using `itertools.tee`. Advance both rolling iterators in sync using `zip`, keeping track of the maximum using `max`.

```python
import itertools
import rolling

WINDOW_SIZE = 500

bids_1, bids_2 = itertools.tee(bids)

roll_max = rolling.Max(bids_1, WINDOW_SIZE)
roll_min = rolling.Min(bids_2, WINDOW_SIZE)

max(hi-lo for hi, lo in zip(roll_max, roll_min))
```

## Ngrams

Count up all substrings with two letters (bigrams) in a sentence and return the five most common.

### Setup

Here's a sentence you may or may not have read before:

```python
sentence = """As a hungry mosquito flies over a steamy swamp a
greedy dragonfly hovers just behind her and behind the dragonfly
waits a famished frog"""
```

### Solution

Convert all two-letter pairs to tuples using `rolling.Apply`. Then use `collection.Counter` to count and then return the most frequent pairs:

```python
from collections import Counter
import rolling

bigrams = rolling.Apply(sentence, window_size=2, operation=tuple)

bigrams_no_spaces = (bigram for bigram in bigrams if ' ' not in bigram)
bigram_freqs = Counter(bigrams_no_spaces)
bigram_freqs.most_common(5)
```

## Too Many Requests

Track incoming requests to a website. If one or more users is responsible for more than a quarter of the last 1000 requests, print a warning message:

### Setup

Here are some strings that look like (not necessarily valid) IP addresses:

```python
def infinite_ip_generator(limit=256):
    population = range(limit)
    while True:
        ints = random.choices(population, k=4)
        yield "{}.{}.{}.{}".format(*ints)

all_ip_addresses = infinite_ip_generator()
```

### Solution

Use `rolling.Mode` to follow the most frequent address in the window and its count. If this count goes above the threshold, print a warning message.

```python
import rolling

WINDOW_SIZE = 1000

for ip_addresses, count in rolling.Mode(all_ip_addresses, WINDOW_SIZE, return_count=True):
    if count > WINDOW_SIZE // 4:
        addresses = ", ".join(ip_addresses)
        print(
            f"Warning: saw {count} requests from IP address(es) {addresses}"
            f" over last {WINDOW_SIZE} requests"
        )
```
(This is obviously just a toy example. There are much better ways to do this on actual web servers.)
