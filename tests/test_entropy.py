import pytest

from rolling.apply import Apply
from rolling.entropy import Entropy, entropy


@pytest.mark.parametrize(
    "sequence,expected",
    [
        ("A", 0),
        ("AB", 1),
        ("ABC", 1.584962500721156),
        ("ABB", 0.9182958340544894),
        ("BAB", 0.9182958340544894),
        ("ABCD", 2),
        ("BADC", 2),
        ("ABCDE", 2.3219280948873626),
        ("ABCDEXX", 2.521640636343319),
    ]
)
def test_entropy(sequence, expected):
    assert entropy(sequence) == pytest.approx(expected)


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
    expected = Apply(sequence, window_size, operation=entropy)
    got = Entropy(sequence, window_size)
    assert pytest.approx(list(got), abs=1e-10) == list(expected)
