from sample_app.calculator import Calculator


def test_add():
    c = Calculator()
    assert c.add(1, 2) == 3


def test_divide_normal():
    c = Calculator()
    assert c.divide(10, 2) == 5


def test_divide_zero_should_raise():
    c = Calculator()
    try:
        c.divide(10, 0)
        assert False, "Expected ValueError"
    except ValueError:
        assert True
