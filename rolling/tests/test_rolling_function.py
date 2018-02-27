import pytest

from rolling import rolling, _rolling_methods, Apply

@pytest.mark.parametrize('name,cls', list(_rolling_methods.items()) + [(set, Apply)])
def test_rolling_function_returns_correct_class_instance(name, cls):
    instance = rolling([], 3, operation=name)
    assert type(instance) is cls

def test_unknown_operation_string():
    with pytest.raises(ValueError) as excinfo:
        rolling([], 10, operation='not_a_real_operation')
    assert str(excinfo.value) == "Unknown rolling operation: 'not_a_real_operation'"

def test_bad_operation_type():
    with pytest.raises(TypeError) as excinfo:
        rolling([], 10, operation=3j)
    assert str(excinfo.value) == "operation must be callable or str, not complex"
