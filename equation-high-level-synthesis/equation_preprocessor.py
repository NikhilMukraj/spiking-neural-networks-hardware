import sys
import re
import ast
import operator as op


if len(sys.argv) < 3:
    print('Too few args...')
    sys.exit(1)

variables = sys.argv[1].split(',')

if any(i.isdigit() or i == '.' for i in variables):
    print('Variables must not be numerical or "."')
    sys.exit(1)

if any(i in ['*', '+', '-', '/', '^'] for i in variables):
    print("Variables must not be operators ('*', '+', '-', '/', '^')")
    sys.exit(1)

if any(len(i) != 1 for i in variables):
    print('Variables must be a single character')
    sys.exit(1)

if 'e' in variables:
    print('"e" is a reserved variable name')
    sys.exit(1)

# https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}
             
def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)

def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """
    return eval_(ast.parse(expr, mode='eval').body)

remove_spaces = lambda x: ''.join(char for char in x if not char.isspace())

exponentation = re.findall(fr'[{"".join(variables)}]\s*\^\s*\d+', sys.argv[2]) # x\s*\^\s*\d+
parsed_exponentation = [remove_spaces(i) for i in exponentation]
print('parsed exponentation: ', parsed_exponentation)

natural_exponentation = re.findall(fr'e\s*\^\s*[{"".join(variables)}]', sys.argv[2])
parsed_natural_exponentation = [remove_spaces(i) for i in natural_exponentation]
print('parsed natural exponentation: ', parsed_natural_exponentation)

negation = re.findall(fr'-\s+[{"".join(variables)}]', sys.argv[2])
parsed_negation = [remove_spaces(i) for i in negation]
print('parsed negation: ', negation)

division_by_constant = re.findall(fr'[{"".join(variables)}]\s*\/\s*\d+', sys.argv[2])
parsed_division_by_constant = [remove_spaces(i) for i in division_by_constant]
print('parsed division: ', parsed_division_by_constant)

constant_exponentation = re.findall(r'\d+\s*\^\s*\d+', sys.argv[2])
print('constant exponentation: ', [eval_expr(remove_spaces(i).replace('^', '**')) for i in constant_exponentation])

constant_addition = re.findall(r'\d+\s*[\+\-]\s*\d+', sys.argv[2])
print('constant addition: ', [eval_expr(remove_spaces(i)) for i in constant_addition])

constant_multiplication = re.findall(r'\d+\s*\*\s*\d+', sys.argv[2])
print('constant multiplication: ', [eval_expr(remove_spaces(i)) for i in constant_multiplication])

constant_division = re.findall(r'\d+\s*/\s*\d+', sys.argv[2])
print('constant division: ', [eval_expr(remove_spaces(i)) for i in constant_division])

# needs to check if float, if float return error
# print('converted exponentation: ', [' * '.join([i.split('^')[0] for _ in range(int(i.split('^')[1]))]) for i in parsed_exponentation])

# 2 : (x*x)
# 3 : (x*x)*x
# 4 : (x*x)*(x*x)
# 5 : ((x*x)*(x*x))*x
# 6 : ((x*x)*(x*x))*(x*x)
# 7 : ((x*x)*(x*x))*(x*x)*x
# 8 : ((x*x)*(x*x))*((x*x)*(x*x))

def recur_exp_string(var, n):
    if n == 2:
        return f'({var}*{var})'
    if n % 2 == 1:
        return recur_exp_string(var, n-1) + f'*{var}'
    else:
        return f'({var}*{var})*' + recur_exp_string(var, n-2)

# for i in range(2,9):
#     print(f'{i}: {recur_exp_string(i)}')

# if float return error
print('converted exponentation: ', recur_exp_string(var, int(i.split('^')[1])))

print('converted negation: ', [f'-1 * {i.split("-")[1]}' for i in parsed_negation])

print('converted division by constant: ', [f'{i.split("/")[0]} * {1 / float(i.split("/")[1])}' for i in parsed_division_by_constant])

# remove operations with converted operations
# add parenethicals to each regex to specify order of operations
#  - change regex to account for () operator ()
# create tree of paranethicals 
# generate variables and modules bottom up
