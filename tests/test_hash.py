from functools import partial

import pytest

from rolling.apply import Apply
from rolling.hash import PolynomialHash, polynomial_hash_sequence, DEF_BASE, DEF_MOD


B = DEF_BASE
M = DEF_MOD


@pytest.mark.parametrize(
    "sequence, expected",
    [
        # fmt: off
        ([3], hash(3)),
        ([3, 1], hash(3)*B + hash(1) % M),
        ([3, 1, 4], hash(3)*B**2 + hash(1)*B + hash(4) % M),
        ([3, 1, 4, 1], hash(3)*B**3 + hash(1)*B**2 + hash(4)*B + hash(1) % M),
        ([3, 1, 4, 1, 5], hash(3)*B**4 + hash(1)*B**3 + hash(4)*B**2 + hash(1)*B + hash(5) % M),
        # fmt: on
    ],
)
def test_polynomial_hash_sequence(sequence, expected):
    assert polynomial_hash_sequence(sequence, base=B, mod=M) == expected


@pytest.mark.parametrize(
    "sequence",
    [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        "AAAAAAAAAAAAAAAAZZZZZZZZ",
        "qwertyuioplkjhgfdsazxcvbnm",
        [3, -8, 1, 7, -2, 4, 7, 2, 1],
        [3, 0, 1, 7, 2],
        [1, 3],
        [],
    ],
)
@pytest.mark.parametrize("window_size", [1, 2, 3, 4, 5, 7])
@pytest.mark.parametrize("window_type", ["fixed", "variable"])
@pytest.mark.parametrize(
    "base, mod", [(DEF_BASE, DEF_MOD), (101, 7919), (5801, 999331)]
)
def test_rolling_polynomial_hash(sequence, window_size, window_type, base, mod):
    got = PolynomialHash(
        sequence, window_size, window_type=window_type, base=base, mod=mod
    )
    func = partial(polynomial_hash_sequence, base=base, mod=mod)
    expected = Apply(sequence, window_size, operation=func, window_type=window_type)
    assert list(got) == list(expected)
