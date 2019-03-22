from collections import defaultdict


class BiCounter(object):
    """
    A dictionary mapping each item to a count,
    and mapping these counts to a set of items.

    Parameters
    ----------

    iterable : any iterable object (optional)
        count the frequencies of items in the iterable

    """

    def __init__(self, iterable=None):
        self.item_to_freq = defaultdict(lambda: 0)
        self.freq_to_items = defaultdict(set)
        self.largest_count = 0
        if iterable:
            for item in iterable:
                self.increment(item)

    def increment(self, item):
        "Increase the count of an item by one"
        freq = self.item_to_freq.get(item, 0)

        if freq > 0:
            self.freq_to_items[freq].remove(item)

        self.freq_to_items[freq + 1].add(item)
        self.item_to_freq[item] += 1
        # if the item was had the largest count, increment largest_count
        if freq == self.largest_count:
            self.largest_count += 1

        # remove the freq if there are no items in the set
        if not self.freq_to_items[freq]:
            del self.freq_to_items[freq]

    def decrement(self, item):
        "Decrease the count of an item by one"
        freq = self.item_to_freq.get(item, 0)
        # if the item in not there already, we are done
        if freq:
            self.freq_to_items[freq].remove(item)

            if freq > 1:
                self.freq_to_items[freq - 1].add(item)
                self.item_to_freq[item] -= 1
            else:
                del self.item_to_freq[item]

            # if the item was the single most common item, decrement the
            # largest_count and then delete the freq key
            if not self.most_common_items:
                self.largest_count -= 1
                del self.freq_to_items[freq]

    @property
    def most_common_items(self):
        return self.freq_to_items[self.largest_count]

    def __iter__(self):
        return iter(self.item_to_freq)

    def __len__(self):
        return len(self.item_to_freq)

    def __contains__(self, item):
        return item in self.item_to_freq

    def __getitem__(self, item):
        return self.item_to_freq[item]

    def __setitem__(self, item, new_freq):
        raise NotImplementedError

    def __delitem__(self, item):
        raise NotImplementedError

    def __bool__(self):
        return bool(self.item_to_freq)
