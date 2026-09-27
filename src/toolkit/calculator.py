class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def top(self):
        return self.items[-1]

    def is_empty(self):
        return self.items == []


def tokenize(expr: str):
    tokens = []
    expr_len = len(expr)
    i = 0

    while i < expr_len:
        if expr[i].isspace():
            i += 1

        elif expr[i] in "+-*/%()":
            tokens.append(("OPERATOR", expr[i]))
            i += 1

        elif expr[i].isdigit():
            start = i
            while i < expr_len and (expr[i].isdigit() or expr[i] == "."):
                i += 1

            tokens.append(("NUMBER", expr[start:i]))

        else:
            raise ValueError(f"Недопустимый символ: {expr[i]}")

    return tokens


def validation(tokens):
    if not tokens:
        raise ValueError("Пустое выражение")

    new_tokens = []
    negative_number = False
    expect_operand = True
    bracket_count = 0

    for i in range(len(tokens)):
        if tokens[i][1] == "(":
            bracket_count += 1
            new_tokens.append(("OPERATOR", tokens[i][1]))

        elif tokens[i][1] == ")":
            if bracket_count == 0:
                raise ValueError("Пропущена открывающая скобка")

            expect_operand = False
            bracket_count -= 1
            new_tokens.append(("OPERATOR", tokens[i][1]))

        elif tokens[i][0] == "NUMBER":
            if not (expect_operand):
                raise ValueError("Пропущенный оператор")

            expect_operand = False
            num = tokens[i][1]
            if negative_number:
                num = "-" + num
                negative_number = False
            new_tokens.append(("NUMBER", num))

        else:
            if expect_operand:
                if tokens[i][1] == "+":
                    pass
                elif tokens[i][1] == "-":
                    negative_number = True
                elif len(new_tokens) != 0 and (
                    new_tokens[-1][1] == tokens[i][1] == "/"
                ):
                    new_tokens.pop()
                    new_tokens.append(("OPERATOR", "//"))
                elif len(new_tokens) != 0 and (
                    new_tokens[-1][1] == tokens[i][1] == "*"
                ):
                    new_tokens.pop()
                    new_tokens.append(("OPERATOR", "**"))
                elif len(new_tokens) != 0:
                    raise ValueError("Два бинарных оператора подряд")
                else:
                    raise ValueError("Пропущенный операнд")

            else:
                expect_operand = True
                new_tokens.append(("OPERATOR", tokens[i][1]))

    if bracket_count != 0:
        raise ValueError("Неправильный формат скобок")
    if expect_operand:
        raise ValueError("Пропущенный операнд")

    return new_tokens


def higher_priority(op1, op2):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "//": 2, "**": 3}
    return precedence[op1] >= precedence[op2]


def compute(num1, num2, operator):
    match operator:
        case "+":
            res = num2 + num1

        case "-":
            res = num2 - num1

        case "*":
            res = num2 * num1

        case "/":
            if num1 == 0:
                raise ZeroDivisionError("Деление на ноль")
            res = num2 / num1

        case "%":
            if num1 == 0:
                raise ZeroDivisionError("Деление на ноль")
            res = num2 % num1

        case "**":
            res = num2**num1

        case "//":
            if num1 == 0:
                raise ZeroDivisionError("Деление на ноль")
            res = num2 // num1

        case _:
            raise ValueError("Неизвестный оператор")

    return res


def parse_number(s):
    if isinstance(s, int | float):
        return s
    return float(s) if "." in s else int(s)


def apply_operator(operator_stack, number_stack):
    operator = operator_stack.pop()
    num1 = parse_number(number_stack.pop())
    num2 = parse_number(number_stack.pop())

    result = compute(num1, num2, operator)
    number_stack.push(result)


def calculate(tokens):
    number_stack = Stack()
    operator_stack = Stack()

    for kind, value in tokens:
        if kind == "NUMBER":
            number_stack.push(value)
            continue

        if value == "(":
            operator_stack.push(value)

        elif value == ")":
            while operator_stack.top() != "(":
                apply_operator(operator_stack, number_stack)
            operator_stack.pop()

        else:
            while (
                not (operator_stack.is_empty())
                and operator_stack.top() != "("
                and higher_priority(operator_stack.top(), value)
            ):
                apply_operator(operator_stack, number_stack)

            operator_stack.push(value)

    while not (operator_stack.is_empty()):
        apply_operator(operator_stack, number_stack)

    return number_stack.pop()
