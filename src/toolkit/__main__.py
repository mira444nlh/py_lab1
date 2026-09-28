import argparse
import sys

from .calculator import evaluate
from .converter import convert


def calc_cmd(args) -> None:
    try:
        print(evaluate(args.expression))

    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(2)

    except ZeroDivisionError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(2)


def convert_cmd(args) -> None:
    try:
        value = float(args.value)
    except ValueError:
        print(f"Неверное числовое значение: {args.value}", file=sys.stderr)
        sys.exit(2)

    try:
        result = convert(value, args.from_arg.lower(), args.to_arg.lower())
        print(result)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(2)


def main() -> None:
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
