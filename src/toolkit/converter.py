from enum import Enum, auto

from .constants import ABSOLUTE_ZERO_CELCIUS


class DegreeUnit(Enum):
    CELCIUS = auto()
    FAHRENHEIT = auto()
    KELVINS = auto()


def unit_to_celcius(degree: float, unit: DegreeUnit) -> float:
    match unit:
        case DegreeUnit.CELCIUS:
            return degree
        case DegreeUnit.FAHRENHEIT:
            return (degree - 32.0) / 1.8
        case DegreeUnit.KELVINS:
            return degree + ABSOLUTE_ZERO_CELCIUS


def celcius_to_unit(degree: float, unit: DegreeUnit) -> float:
    match unit:
        case DegreeUnit.CELCIUS:
            return degree
        case DegreeUnit.FAHRENHEIT:
            return degree * 1.8 + 32.0
        case DegreeUnit.KELVINS:
            return degree - ABSOLUTE_ZERO_CELCIUS


def convert(value: float, unit_from: str, unit_to: str) -> float:
    categories = {
        "mm": 1,
        "cm": 1,
        "m": 1,
        "km": 1,
        "g": 2,
        "kg": 2,
        "c": 3,
        "f": 3,
        "k": 3,
    }

    length_mass_convert = {
        "mm": 100000,
        "cm": 10000,
        "m": 1000,
        "km": 1,
        "g": 1000,
        "kg": 1,
    }

    degree_units = {
        "c": DegreeUnit.CELCIUS,
        "f": DegreeUnit.FAHRENHEIT,
        "k": DegreeUnit.KELVINS,
    }

    if unit_from not in categories:
        raise ValueError(f"Неизвестная единица: {unit_from}")
    if unit_to not in categories:
        raise ValueError(f"Неизвестная единица: {unit_to}")
    if categories[unit_from] != categories[unit_to]:
        raise ValueError("Несовместимые единицы")

    if categories[unit_from] in (1, 2):
        return value / length_mass_convert[unit_from] * length_mass_convert[unit_to]

    celcius_degree = unit_to_celcius(value, degree_units[unit_from])
    if celcius_degree < ABSOLUTE_ZERO_CELCIUS:
        raise ValueError("Температура ниже абсолютного нуля")

    return celcius_to_unit(celcius_degree, degree_units[unit_to])
