import argparse
import sys

from toolkit.calculator import evaluate
from toolkit.converter import convert, parse_value
from toolkit.errors import CalculatorError, ConverterError


def calc_cmd(args) -> None:
    """Handle the 'calc' command."""
    try:
        print(evaluate(args.expression))

    except CalculatorError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(2)

    except ZeroDivisionError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(2)


def convert_cmd(args) -> None:
    """Handle the 'convert' command."""
    try:
        value = parse_value(args.value)
        result = convert(value, args.from_arg.lower(), args.to_arg.lower())
        print(result)
    except ConverterError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(2)


def main() -> None:
    """Build the argument parser and run the selected command."""
    parser = argparse.ArgumentParser(description="Калькулятор и конвертер величин")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Доступные команды"
    )

    calc_parser = subparsers.add_parser("calc", help="Вычислить выражение")
    calc_parser.add_argument("expression", help="Выражение")
    calc_parser.set_defaults(func=calc_cmd)

    convert_parser = subparsers.add_parser("convert", help="Конвертировать величину")
    convert_parser.add_argument("value", help="Величина")
    convert_parser.add_argument(
        "--from", dest="from_arg", required=True, help="Изначальные единицы измерения"
    )
    convert_parser.add_argument(
        "--to", dest="to_arg", required=True, help="Конечные единицы измерения"
    )
    convert_parser.set_defaults(func=convert_cmd)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
