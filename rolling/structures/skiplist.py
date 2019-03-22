"""
This code is taken from Raymond Hettinger's recipe for
indexable skiplist solution to the rolling median problem.
Only very minor modifications have been made to the code
(e.g. to make it compatible with Python 3).

    http://code.activestate.com/recipes/576930/

There is also discussion and an alternative implementation
to be found at the following links:

    https://rhettinger.wordpress.com/2010/02/06/lost-knowledge/
    http://code.activestate.com/recipes/577073/

The Indexable aproach is also used in the pandas library and
I referred to the implementation there also:

    github.com/pandas-dev/pandas/blob/master/pandas/_libs/src/skiplist.h
    github.com/pandas-dev/pandas/blob/master/pandas/_libs/window.pyx#L1055-L1129
    github.com/pandas-dev/pandas/blob/master/pandas/_libs/skiplist.pyx
    github.com/pandas-dev/pandas/blob/master/pandas/_libs/skiplist.pxd

The indexable skiplist allows O(log k) insertions and deletions
and allows a value to be retrieved by rank.

"""
from random import random
from math import log, ceil


class Node(object):
    __slots__ = "value", "next", "width"

    def __init__(self, value, next, width):
        self.value, self.next, self.width = value, next, width


class End(object):
    """
    Sentinel object that always compares greater than another object
    """

    def __gt__(self, other):
        return True

    def __lt__(self, other):
        return False

    __ge__ = __gt__
    __le__ = __lt__


NIL = Node(End(), [], [])


class IndexableSkiplist(object):
    """
    Sorted collection supporting O(lg n) insertion, removal, and lookup by rank.
    """

    def __init__(self, expected_size):
        self.size = 0
        self.maxlevels = int(1 + log(expected_size, 2))
        self.head = Node("HEAD", [NIL] * self.maxlevels, [1] * self.maxlevels)

    def __getitem__(self, i):
        node = self.head
        i += 1
        for level in reversed(range(self.maxlevels)):
            while node.width[level] <= i:
                i -= node.width[level]
                node = node.next[level]
        return node.value

    def insert(self, value):
        # find first node on each level where node.next[levels].value > value
        chain = [None] * self.maxlevels
        steps_at_level = [0] * self.maxlevels
        node = self.head
        for level in reversed(range(self.maxlevels)):
            while node.next[level].value <= value:
                steps_at_level[level] += node.width[level]
                node = node.next[level]
            chain[level] = node

        # insert a link to the newnode at each level
        d = min(self.maxlevels, 1 - int(log(random(), 2.0)))
        newnode = Node(value, [None] * d, [None] * d)
        steps = 0
        for level in range(d):
            prevnode = chain[level]
            newnode.next[level] = prevnode.next[level]
            prevnode.next[level] = newnode
            newnode.width[level] = prevnode.width[level] - steps
            prevnode.width[level] = steps + 1
            steps += steps_at_level[level]
        for level in range(d, self.maxlevels):
            chain[level].width[level] += 1
        self.size += 1

    def remove(self, value):
        # find first node on each level where node.next[levels].value >= value
        chain = [None] * self.maxlevels
        node = self.head
        for level in reversed(range(self.maxlevels)):
            while node.next[level].value < value:
                node = node.next[level]
            chain[level] = node
        if value != chain[0].next[0].value:
            raise KeyError("Not Found")

        # remove one link at each level
        d = len(chain[0].next[0].next)
        for level in range(d):
            prevnode = chain[level]
            prevnode.width[level] += prevnode.next[level].width[level] - 1
            prevnode.next[level] = prevnode.next[level].next[level]
        for level in range(d, self.maxlevels):
            chain[level].width[level] -= 1
        self.size -= 1
