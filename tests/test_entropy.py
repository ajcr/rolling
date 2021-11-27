from collections import Counter
from math import fsum, log2

import pytest

from rolling.apply import Apply
from rolling.entropy import Entropy


def _entropy(seq):
    N = len(seq)
    counts = Counter(seq)
    return -fsum((c / N) * log2(c / N) for c in counts.values())


@pytest.mark.parametrize("window_size", [1, 3, 5, 7, 10])
@pytest.mark.parametrize(
    "sequence",
    [
        "qqqqqqqq",
        "xxxyxyyxyxyxx",
        "asabsdhvshsfhohdshdsfohwefsdfasbdbbdbbasdssabbsbsbsbasdbd",
        "cucumber",
        "foo...bar",
        "cupcupspoonspoon knife",
    ],
)
def test_rolling_entropy(window_size, sequence):
    expected = Apply(sequence, window_size, operation=_entropy)
    got = Entropy(sequence, window_size)
    assert pytest.approx(list(got), abs=1e-10) == list(expected)


def test_rolling_entropy_raises_for_variable():
    with pytest.raises(NotImplementedError):
        Entropy("abcde", 5, window_type="variable")
