import pytest

from rolling.apply import Apply
from rolling.matching import Match


@pytest.mark.parametrize(
    "match",
    [
        ["i"],
        ["m", "i"],
        ["lo"],
        ["on", "it", "is"],
        ["sum"],
        ["sec", "act", "cat", "rat"],
        ["dolor"],
    ],
)
def test_rolling_match_strings(match):
    SEQUENCE = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    got = Match(SEQUENCE, match)
    func = lambda window: "".join(window) in match
    expected = Apply(SEQUENCE, len(match[0]), operation=func)
    assert list(got) == list(expected)


@pytest.mark.parametrize(
    "match",
    [
        [[0]],
        [[1]],
        [[2, 3], [3, 2]],
        [[1, 4, 5, 6]],
        [[1, 4, 5, 6, 7], [1, 1, 1, 1, 2]],
    ],
)
def test_rolling_match_integers(match):
    SEQUENCE = [1, 3, 1, 4, 5, 6, 7, 3, 2]
    got = Match(SEQUENCE, match)
    func = lambda window: list(window) in match
    expected = Apply(SEQUENCE, len(match[0]), operation=func)
    assert list(got) == list(expected)
