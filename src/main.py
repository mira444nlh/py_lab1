import argparse
import sys
from src.calculator import calculate, validation, tokenize

def calc_cmd(args):
    try:
        tokens = tokenize(args.expression)
        validated_tokens = validation(tokens)
        result = calculate(validated_tokens)
        print(result)

    except ValueError as e:
       print(f"Ошибка: {e}")
       sys.exit(2)

    except ZeroDivisionError as e:
       print(f"Ошибка: {e}")
       sys.exit(2)


def convert_cmd(args):
    pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Калькулятор и конвертер величин")
    subparsers = parser.add_subparsers(dest="command", required = True, help="Доступные команды")

    calc_parser = subparsers.add_parser("calc", help="Вычислить выражение")
    calc_parser.add_argument("expression", help="Выражение")
    calc_parser.set_defaults(func=calc_cmd)

    convert_parser = subparsers.add_parser("convert", help="Конвертировать величину")
    convert_parser.add_argument("value", help="Величина")
    convert_parser.add_argument("--from", required = True, help="Изначальные единицы измерения")
    convert_parser.add_argument("--to", required = True, help="Конечные единицы измерения")
    convert_parser.set_defaults(func=convert_cmd)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
