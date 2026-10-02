class ToolkitError(Exception):
    pass

# calculator error
class CalculatorError(ToolkitError):
    pass

class EmptyExpressionError(CalculatorError):
    pass

class InvalidCharacterError(CalculatorError):
    pass

class MissedOperandError(CalculatorError):
    pass

class MissedOperatorError(CalculatorError):
    pass

class TwoBinaryOperatorsInRowError(CalculatorError):
    pass

class InvalidBracketsFormatError(CalculatorError):
    pass


# converter error
class ConverterError(ToolkitError):
    pass

class InvalidValueError(ConverterError):
    pass

class UnknownUnitError(ConverterError):
    pass

class IncompatibleUnitsError(ConverterError):
    pass

class DegreeLowerThanAbsoluteZeroError(ConverterError):
    pass
