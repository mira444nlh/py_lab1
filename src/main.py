import argparse
from src.calculator import calculate, tokenize

def calc_cmd(args):
    tokens = tokenize(args.expression)
    result = calculate(tokens)
    print(result)

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
