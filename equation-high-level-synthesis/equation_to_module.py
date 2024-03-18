import sys
import os
import string
import json
import re
from fixed_point_models import decimal_to_fixed_point


GREEN = '\033[1;32m'
NC = '\033[0m'
RED = '\033[0;31m'

if len(sys.argv) < 2:
    print(f'{RED}Too few args...{NC}')
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    args = json.load(f)

necessary_args = {
    'name': [str],
    'equation': [str],
    'variables': [list],
    'out_variable': [str],
    'integer_bits': [int],
    'integer_bits': [int],
    'lower_bound': [int, float],
    'upper_bound': [int, float],
    'tolerance': [int, float],
}

for key, value in necessary_args.items():
    if key not in args:
        print(f'{RED}"{key}" not found{NC}')
        sys.exit(1)
    if type(args[key]) not in value:
        print(f'{RED}"{key}" is of type "{type(args[key])}" not {value}{NC}')
        sys.exit(1)

if any(type(i) != str for i in args['variables']):
    print(f'{RED}All items in "variables" must be strings{NC}')
    sys.exit(1)

if any(i == 'e' for i in args['variables']):
    print(f'{RED}"e" is a reserved variable name{NC}')
    sys.exit(1)

module_name = args['name']

if any(i not in string.ascii_letters + string.digits + '_' for i in module_name):
    print(f'{RED}All characters in "module_name" must be alphanumeric{NC}')
    sys.exit(1)

piecewise_vars = ['m1', 'm2', 'b1', 'b2', 'split']
valid_piecewise_vars = sum([i in args for i in piecewise_vars])

if valid_piecewise_vars == len(piecewise_vars):
    do_piecewise = True
elif valid_piecewise_vars == 0:
    do_piecewise = False
else:
    print(f'{RED}Must enter a value for "m1", "m2", "b1", "b2", and "split" if using piecewise{NC}')
    sys.exit(1)

if do_piecewise and any([type(args[i]) not in [float, int] for i in piecewise_vars]):
    print(f'{RED}Value for "m1", "m2", "b1", "b2", and "split" must be "float" or "int" if using piecewise{NC}')
    sys.exit(1)

if 'generate_floats' in args and type(args['generate_floats']) == bool:
    generation_type = 'uniform' if args['generate_floats'] else 'randint'
elif 'generate_floats' in args and type(args['generate_floats']) != bool:
    print(f'{RED}"generate_floats" argument must be a boolean{NC}')
    sys.exit(1)
else:
    generation_type = 'randint'

eq = args['equation']
integer_bits = args['integer_bits']
fractional_bits = args['fractional_bits']
N = integer_bits + fractional_bits
variables = args['variables']
out_variable = args['out_variable']
lower_bound, upper_bound = args['lower_bound'], args['upper_bound']
tolerance = args['tolerance']

add_module = lambda n, a, b, c: f'add adder{n} ( {a}, {b}, {c} );'
basic_mult_module = lambda n, a, b, c: f'mult multiplier{n} ( {a}, {b}, {c} );'
negator_module = lambda n, a, c:  f'negator negator{n} ( {a}, {c} );'

binary_negative_one = f"{N}'b{decimal_to_fixed_point(-1, integer_bits, fractional_bits)}"

def mult_module(n, a, b, c):
    if a != binary_negative_one and b != binary_negative_one:
        return basic_mult_module(n, a, b, c)
    elif a == binary_negative_one:
        return negator_module(n, b, c)
    elif b == binary_negative_one:
        return negator_module(n, a, c)

div_module = lambda n, a, b, c: f'div divider{n} ( {a}, {b}, {c} );'

num_to_binary_string = lambda string: f"{N}'b{decimal_to_fixed_point(float(string), integer_bits, fractional_bits)}"

def convert_decimals(string):
    if re.match(r'^-*(\d|\.)+$', string):
        return num_to_binary_string(string)
    else: 
        return string

def exp_module(n, a, b, c):
    if a != 'e':
        raise ValueError('Can only use "e" as base exponent')

    if not do_piecewise:
        return f'exp exponentiate{n} ( {b}, {c} );' # negative exp option if a = neg_e
    if do_piecewise:
        m1 = num_to_binary_string(args['m1'])
        b1 = num_to_binary_string(args['b1'])
        m2 = num_to_binary_string(args['m2'])
        b2 = num_to_binary_string(args['b2'])
        split = num_to_binary_string(args['split'])

        return f'linear_piecewise piecewise{n} ( {b}, {m1}, {m2}, {b1}, {b2}, {split}, {c} );'

def abs_module(n, a, b, c):
    if a != 'abs':
        raise ValueError('Must specify "|" operator is "abs"')
    
    return f'abs absolute_value{n} ( {b}, {c} );'

func_modules = {
    '+' : add_module, 
    '*' : mult_module,
    '/' : div_module,
    '^' : exp_module,
    '|' : abs_module,
}

module_types = {
    '+' : 'adder',
    '*' : 'mult',
    '/' : 'div',
    '^' : 'exp',
    '|' : 'abs',
}

def module_type_length(modules, module_type):
    return len([i for i in modules if module_type in i]) + 1

def get_operator(string):
    if '+' in string:
        return '+'
    elif '*' in string:
        return '*'
    elif '/' in string:
        return '/'
    elif '^' in string:
        return '^'
    elif '|' in string:
        return '|'

    raise ValueError('Operator not found') 

def parenthetic_contents(string):
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])

parsed = list(parenthetic_contents(eq))
print(parsed)

parsed.sort(key=lambda x: x[0])
print(parsed)

max_depth = max(parsed, key=lambda x: x[0])[0]
lowest = [i for i in parsed if i[0] == max_depth]

modules = []
intermediates = {}

def update_modules(modules, op, first, second, out, comment):
    module_to_use = func_modules[op]
    n = module_type_length(modules, module_types[op])
    generated_module = module_to_use(n, first, second, out)
    modules.append(generated_module + f' // {comment}')

for _, i in lowest:
    intermediates[i] = f'term{len(intermediates)+1}'

    op = get_operator(i)

    first, second = [convert_decimals(i) for i in i.split(op)]

    update_modules(modules, op, first, second, intermediates[i], i)

for n in range(max_depth-1, -1, -1):
    level = [i for i in parsed if i[0] == n]

    for _, i in level:
        pre_replacement = i
        intermediates[i] = f'term{len(intermediates)+1}'

        for _, key in parsed:
            print('key:', key, '| i:', i)
            if key in i and i != key:
                i = i.replace(key, intermediates[key])

        op = get_operator(i)

        print(i.split(op), op, key)
        first, second = i.split(op)
        first = first.strip('()')
        second = second.strip('()')
        first, second = [convert_decimals(i) for i in (first, second)]

        update_modules(modules, op, first, second, intermediates[pre_replacement], pre_replacement)

print(modules)
print(intermediates)

last_term_key = list(intermediates.keys())[-1]
last_term = intermediates[last_term_key]
del intermediates[last_term_key]
modules = [i if last_term not in i else i.replace(last_term, out_variable) for i in modules]

module_variables = ",\n\t".join(["input [N-1:0] " + i for i in variables])
include_string = '`include "../ops.sv"\n\n\n'
module_header = f'module {module_name} #(\n\tparameter N={N},\n\tparameter Q={fractional_bits}\n)(\n\t{module_variables},\n\toutput [N-1:0] {out_variable} \n);\n\t'
intermediates_string = 'wire [N-1:0] ' + ', '.join(intermediates.values()) + ';\n\n\t'
modules_string = '\n\t'.join(modules)
verilog_file = include_string + module_header + intermediates_string + modules_string + '\nendmodule\n'
print(verilog_file)

generate_random_vars = '\n\t'.join(f'{i} = np.random.{generation_type}(lower_bound, upper_bound)' for i in variables)
generate_binary_values = '\n\t'.join(f'binary_{i} = decimal_to_fixed_point({i}, int_bits, frac_bits)' for i in variables)
generate_setting_values = '\n\t'.join(f'dut.{i}.value = BinaryValue(binary_{i})' for i in variables)

if any('exp' in i or 'linear_piecewise' in i for i in modules):
    eq = re.sub(r'e\W*\^', 'np.exp', eq)
if any('abs' in i for i in modules):
    eq = re.sub(r'abs\W*\|', 'np.abs', eq)

test_file = f'''import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import check_with_tolerance
import numpy as np


@cocotb.test()
async def test(dut):
    int_bits = {integer_bits}
    frac_bits = {fractional_bits}
    lower_bound, upper_bound = {lower_bound}, {upper_bound}
    tolerance = {tolerance}

    for i in range(100):
        {generate_random_vars}

        {generate_binary_values}    
        {generate_setting_values}

        await Timer(2, units="ns")

        output_value = fixed_point_to_decimal(str(dut.{out_variable}.value), int_bits, frac_bits)
        actual = {eq}

        assert check_with_tolerance(
            actual,
            output_value, 
            {tolerance}
        ), f'{{actual}} != {{output_value}}'
'''

test_file = test_file.replace('\t', '        ')

print(test_file)

makefile = f'''# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/{module_name}.sv
# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = {module_name}

# MODULE is the basename of the Python test file
MODULE = {module_name}_test

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
'''

print(makefile)

os.mkdir(f'module-{module_name}')
with open(f'./module-{module_name}/Makefile', 'w+') as f:
    f.write(makefile)
with open(f'./module-{module_name}/{module_name}.sv', 'w+') as f:
    f.write(verilog_file)
with open(f'./module-{module_name}/{module_name}_test.py', 'w+') as f:
    f.write(test_file)

print(f'{GREEN}Finished writing modules{NC}')

# TODO:
# equation preprocessing
# - perform regex parsing and simplification
#   - when parsing exponentation, output should be ((x * x) * x) if odd, (x * x) * (x * x) if even
# - potentially could do a round of simplifcation with sympy beforehand and then do regex
# - FIRST: translate number into fixed point number given amount of integer and fractional bits
#   - regex: -*(\d|\.)+
#   - convert numbers after modules are created
# - determine right amount of parantheticals
# - turn subtraction into negation then addition
# generate comments for each module
# - comment every time a number is converted to binary with its numerical equavilent
# handle re-using of terms efficiently 
# - there may be specific order in which repeated terms can be inputted, (re-used second position)
# handle division
# handle e^x
# automatic test creation through cocotb with makefile
