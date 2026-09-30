import pytest

from toolkit.constants import ABSOLUTE_ZERO_CELCIUS
from toolkit.converter import convert


# positive tests
def test_length_m_to_km():
    assert convert(1000, "m", "km") == 1.0


def test_length_km_to_mm():
    assert convert(1.0, "km", "mm") == 100000.0


def test_mass_kg_to_g():
    assert convert(1, "kg", "g") == 1000.0


def test_temperature_celsius_to_fahrenheit():
    assert convert(0, "c", "f") == pytest.approx(32)


def test_temperature_celsius_to_kelvin():
    result = convert(0, "c", "k")
    assert result == pytest.approx(-ABSOLUTE_ZERO_CELCIUS)


def test_temperature_fahrenheit_to_celsius():
    assert convert(32, "f", "c") == pytest.approx(0)


def test_same_unit_returns_same_value():
    assert convert(420, "m", "m") == 420.0


# negative tests
def test_unknown_unit_from_raises_value_error():
    with pytest.raises(ValueError):
        convert(1, "xx", "m")


def test_unknown_unit_to_raises_value_error():
    with pytest.raises(ValueError):
        convert(1, "m", "xx")


def test_incompatible_categories_raise_value_error():
    with pytest.raises(ValueError):
        convert(1, "m", "kg")


def test_temperature_below_absolute_zero_raises_value_error():
    with pytest.raises(ValueError):
        convert(ABSOLUTE_ZERO_CELCIUS - 1, "c", "f")
