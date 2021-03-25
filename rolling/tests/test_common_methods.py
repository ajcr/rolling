from rolling import Apply


def test_extend_iterator_fixed_window_size_1():
    seq = [0, 1]
    roll = Apply(seq, 1, operation=list)

    assert next(roll) == [0]
    assert next(roll) == [1]
    assert next(roll, None) is None

    # extend after iterable has been exhausted
    roll.extend([2, 3])
    assert next(roll) == [2]

    # extend while iterable is still running
    roll.extend([4])
    assert next(roll) == [3]
    assert next(roll) == [4]
    assert next(roll, None) is None


def test_extend_iterator_fixed_window_size_3():
    seq = [0, 1, 2]
    roll = Apply(seq, 3, operation=list)

    assert next(roll) == [0, 1, 2]
    assert next(roll, None) is None

    # extend after iterable has been exhausted
    roll.extend([3, 4])
    assert next(roll) == [1, 2, 3]

    # extend while iterable is still running
    roll.extend([5])
    assert next(roll) == [2, 3, 4]
    assert next(roll) == [3, 4, 5]
    assert next(roll, None) is None


def test_extend_iterator_fixed_window_size_3_original_too_short():
    seq = [0, 1]
    roll = Apply(seq, 3, operation=list)
    assert next(roll, None) is None

    roll.extend([2, 3])
    assert next(roll) == [0, 1, 2]
    assert next(roll) == [1, 2, 3]
    assert next(roll, None) is None


def test_extend_iterator_variable_window_size_3():
    seq = [0, 1]
    roll = Apply(seq, 3, window_type="variable", operation=list)

    assert next(roll) == [0]
    assert next(roll) == [0, 1]

    # extend while window is growing
    roll.extend([2])
    assert next(roll) == [0, 1, 2]

    # extend while the window is at full size
    roll.extend([3, 4])
    assert next(roll) == [1, 2, 3]
    assert next(roll) == [2, 3, 4]
    assert next(roll) == [3, 4]

    # extend while the window is shrinking
    roll.extend([5, 6])
    assert next(roll) == [3, 4, 5]
    assert next(roll) == [4, 5, 6]
    assert next(roll) == [5, 6]
    assert next(roll) == [6]
    assert next(roll, None) is None

    # extend after the iterator has been exhausted
    roll.extend([7, 8])
    assert next(roll) == [6, 7]
    assert next(roll) == [6, 7, 8]
    assert next(roll) == [7, 8]
    assert next(roll) == [8]
