import pytest

from rolling.apply import Apply


@pytest.mark.parametrize("window_type", ["bad_type", 121, tuple])
def test_unknown_window_type_type_raises(window_type):
    with pytest.raises(ValueError):
        Apply([], 5, window_type=window_type)


@pytest.mark.parametrize("window_size", [0, -21])
def test_bad_window_size_value_raises(window_size):
    with pytest.raises(ValueError):
        Apply([], window_size)


@pytest.mark.parametrize("window_size", ["bad_type", 21.3, tuple])
def test_bad_window_size_type_raises(window_size):
    with pytest.raises(TypeError):
        Apply([], window_size)
