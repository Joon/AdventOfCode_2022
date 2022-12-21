from sympy import sympify,solve,symbols
from sympy.parsing.sympy_parser import parse_expr

file = open('day21_input.txt', 'r')
lines = [s.strip() for s in file.readlines()]

operations = {l.split(': ')[0]: l.split(': ')[1] for l in lines}

def build_statement(monkey, special=None):
    if special is not None and monkey == special:
        return monkey

    if operations[monkey].strip().isnumeric():
        return operations[monkey].strip()
    else:
        lhs, operation, rhs = operations[monkey].strip().split(' ')
        statement_addition = f"({build_statement(lhs, special)} {operation} {build_statement(rhs, special)})"
        try:
            value = eval(statement_addition)
            return str(value)
        except:
            return statement_addition

print("Answer 1", eval(build_statement('root')))

lhs, operation, rhs = operations['root'].strip().split(' ')
answer_formula_left = build_statement(lhs, 'humn').replace(".0", "")
answer_formula_right = build_statement(rhs, 'humn').replace(".0", "")

print("Equality to answer part 2", parse_expr(answer_formula_left), ' = ', parse_expr(answer_formula_right))
