import pytest

from toolkit.calculator import evaluate


# positive tests
def test_single_number():
    assert evaluate("2") == 2


def test_addition():
    assert evaluate("2+2") == 4


def test_operator_precedence():
    assert evaluate("2+3*4") == 14


def test_parentheses_change_precedence():
    assert evaluate("(2+3)*4") == 20


def test_float_numbers():
    assert evaluate("2.5+2.5") == 5.0


def test_unary_minus():
    assert evaluate("-5+3") == -2


def test_unary_plus():
    assert evaluate("5-+3") == 2


def test_power_operator():
    assert evaluate("2**3") == 8


def test_floor_division_operator():
    assert evaluate("7//2") == 3


def test_modulo_operator():
    assert evaluate("7%2") == 1


def test_nested_parentheses():
    assert evaluate("((1+2)*(3+4))") == 21


def test_unary_minus_behind_parentheses():
    assert evaluate("-(-5)") == 5


# negative tests
def test_division_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        evaluate("5/0")


def test_modulo_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        evaluate("5%0")


def test_floor_division_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        evaluate("5//0")


def test_invalid_character_raises_value_error():
    with pytest.raises(ValueError):
        evaluate("2+2a")


def test_empty_expression_raises_value_error():
    with pytest.raises(ValueError):
        evaluate("")


def test_two_operators_in_a_row_raises_value_error():
    with pytest.raises(ValueError):
        evaluate("2*/2")


def test_not_closed_parentheses_raises_value_error():
    with pytest.raises(ValueError):
        evaluate("(2+2")


def test_not_opened_parentheses_raises_value_error():
    with pytest.raises(ValueError):
        evaluate("2+2)")


def test_missing_operand_raises_value_error():
    with pytest.raises(ValueError):
        evaluate("2+")
