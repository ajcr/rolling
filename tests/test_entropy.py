import functools

import pytest

from rolling.apply import Apply
from rolling.entropy import Entropy, entropy


TEST_REFERENCE_DISTRIBUTION = {
    "A": 1/12,
    "B": 3/12,
    "C": 2/12,
    "D": 1/12,
    "E": 4/12,
    "X": 1/12,
}


@pytest.mark.parametrize(
    "sequence,expected,reference_distribution",
    [
        ("A", 0, None),
        ("AB", 1, None),
        ("ABC", 1.584962500721156, None),
        ("ABB", 0.9182958340544894, None),
        ("BAB", 0.9182958340544894, None),
        ("ABCD", 2, None),
        ("BADC", 2, None),
        ("ABCDE", 2.3219280948873626, None),
        ("ABCDEXX", 2.521640636343319, None),
        ("A", 3.584962500721156, TEST_REFERENCE_DISTRIBUTION),
        ("AB", 1.7924812503605783, TEST_REFERENCE_DISTRIBUTION),
        ("ABCDEXX", 0.408327221417673, TEST_REFERENCE_DISTRIBUTION),
    ]
)
def test_entropy(sequence, expected, reference_distribution):
    assert entropy(sequence, 2, reference_distribution) == pytest.approx(expected)


@pytest.mark.parametrize("window_size", [1, 3, 5, 7, 10, 15])
@pytest.mark.parametrize(
    "sequence",
    [
        "AAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "AAAAAAAAAXXXXXAAAAAAAAAAAAA",
        "XXXDXDDXDXDXX",
        "ABBCCBBEBEEBCEBCAXXXABCBCBBCBCBCBCBBBBBBCCCAAAAAAAAAABBBB",
        "EEEEEEEEEEEEEEEEEEXXXXCACACACXXXXXXXXCCADACCCCCAAAAAACCCACACXX",
        "CACAXDEB",
        "AAAAAABBCCCBCB",
        "DDDDDDXXXXXXXXXXAAAAAAAAABCABCABCABCA",
        "ABCDEXABCDEXABCDEXABCDEXABCDEX",
    ],
)
@pytest.mark.parametrize("base", [2, 10, "e", 7])
@pytest.mark.parametrize("reference_distribution", [None, TEST_REFERENCE_DISTRIBUTION])
def test_rolling_entropy(window_size, sequence, base, reference_distribution):
    entropy_ = functools.partial(entropy, base=base, reference_distribution=reference_distribution)
    expected = Apply(sequence, window_size, operation=entropy_)
    got = Entropy(sequence, window_size, base=base, reference_distribution=reference_distribution)
    assert pytest.approx(list(got), abs=1e-10) == list(expected)
