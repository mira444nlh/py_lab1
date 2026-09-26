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
        return (self.items == [])


def tokenize(expr: str):
    # TODO implement unary operators
    tokens = []
    expr_len = len(expr)
    i = 0

    while i < expr_len:
        if expr[i].isspace():
            i += 1

        elif expr[i] in '+-*/()':
            tokens.append(('OPERATOR', expr[i]))
            i += 1

        elif expr[i].isdigit():
            start = i
            while i < expr_len and (expr[i].isdigit() or expr[i] == '.'):
                i += 1

            tokens.append(('NUMBER', expr[start:i]))


        else:
            raise ValueError(f"Неизвестный символ: {expr[i]}")

    return tokens

def higher_priority(op1, op2):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    return precedence[op1] >= precedence[op2]

def compute(num1, num2, operator):
    match operator:
        case '+':
            res = num2 + num1

        case '-':
            res = num2 - num1

        case '*':
            res = num2 * num1

        case '/':
            res = num2 / num1

        case _:
            res = 0

    return res

def parse_number(s):
    if isinstance(s, int | float):
        return s
    return float(s) if '.' in s else int(s)

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
        if kind == 'NUMBER':
            number_stack.push(value)
            continue

        while not(operator_stack.is_empty()) and higher_priority(operator_stack.top(), value):
            apply_operator(operator_stack, number_stack)

        operator_stack.push(value)

    while not(operator_stack.is_empty()):
        apply_operator(operator_stack, number_stack)

    return number_stack.pop()
