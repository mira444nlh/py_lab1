class Stack:
    """LIFO stack based on a list."""

    def __init__(self):
        """Create an empty stack."""
        self.items = []

    def push(self, item):
        """Put an item on top of the stack."""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item."""
        return self.items.pop()

    def top(self):
        """Return the top item without removing it."""
        return self.items[-1]

    def is_empty(self):
        """Return True if the stack has no items."""
        return self.items == []


def tokenize(expr: str) -> list[tuple[str, str]]:
    """Split an expression into (kind, value) tokens."""
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


def validation(tokens: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Check token order and brackets, fold unary signs and merge '//' and '**'."""
    if not tokens:
        raise ValueError("Пустое выражение")

    new_tokens = []
    negative_number = False
    expect_operand = True
    bracket_count = 0

    for key, value in tokens:
        if value == "(":
            bracket_count += 1
            new_tokens.append(("OPERATOR", value))

        elif value == ")":
            if bracket_count == 0:
                raise ValueError("Неправильный формат скобок")

            expect_operand = False
            bracket_count -= 1
            new_tokens.append(("OPERATOR", value))

        elif key == "NUMBER":
            if not (expect_operand):
                raise ValueError("Пропущенный оператор")

            expect_operand = False
            num = value
            if negative_number:
                num = "-" + num
                negative_number = False
            new_tokens.append(("NUMBER", num))

        else:
            if expect_operand:
                if value == "+":
                    pass
                elif value == "-":
                    negative_number = not negative_number
                elif len(new_tokens) != 0 and (
                    new_tokens[-1][1] == value == "/"
                ):
                    new_tokens.pop()
                    new_tokens.append(("OPERATOR", "//"))
                elif len(new_tokens) != 0 and (
                    new_tokens[-1][1] == value == "*"
                ):
                    new_tokens.pop()
                    new_tokens.append(("OPERATOR", "**"))
                elif len(new_tokens) != 0:
                    raise ValueError("Два бинарных оператора подряд")
                else:
                    raise ValueError("Пропущенный операнд")

            else:
                expect_operand = True
                new_tokens.append(("OPERATOR", value))

    if bracket_count != 0:
        raise ValueError("Неправильный формат скобок")
    if expect_operand:
        raise ValueError("Пропущенный операнд")

    return new_tokens


def higher_priority(op1: str, op2: str) -> bool:
    """Return True if op1 has precedence greater than or equal to op2."""
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "//": 2, "**": 3}
    return precedence[op1] >= precedence[op2]


def compute(num1: float, num2: float, operator: str) -> int | float:
    """Apply a binary operator to num2 and num1."""
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


def parse_number(s: str | float) -> int | float:
    """Convert a numeric string to int or float; return numbers unchanged."""
    if isinstance(s, int | float):
        return s
    return float(s) if "." in s else int(s)


def apply_operator(operator_stack: Stack, number_stack: Stack) -> None:
    """Pop one operator and two numbers, then push the computed result."""
    operator = operator_stack.pop()
    num1 = parse_number(number_stack.pop())
    num2 = parse_number(number_stack.pop())

    result = compute(num1, num2, operator)
    number_stack.push(result)


def calculate(tokens: list[tuple[str, str]]) -> int | float:
    """Evaluate validated tokens using two stacks."""
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


def evaluate(expression: str) -> int | float:
    """Tokenize, validate and calculate an arithmetic expression string."""
    tokens = tokenize(expression)
    validated_tokens = validation(tokens)
    result = parse_number(calculate(validated_tokens))
    return result
