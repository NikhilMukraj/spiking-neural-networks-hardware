import sys
import json
import re
from fixed_point_models import decimal_to_fixed_point


# GREEN = '\033[1;32m'
# NC = '\033[0m'
# RED = '\033[0;31m'

# get rid of previous arg declarations
# if len(sys.argv) < 2:
#     print(f'{RED}Too few args...{NC}')
#     sys.exit(1)

# with open(sys.argv[1], 'r') as f:
#     args = json.load(f)

# necessary_args = {
#     'name': str,
#     'eq': str,
#     'variables': list,
    # 'out_variable': str,
#     'integer_bits': int,
#     'integer_bits': int,
#     'lower_bound': (int, float),
#     'upper_bound': (int, float),
#     'tolerance': (int, float),
# }

# for key, value in necessary_args.items():
#     if key not in args:
#         print(f'{RED}"{key}" not found{NC}')
#         sys.exit(1)
#     if type(args[key]) != value:
#         print(f'{RED}"{key}" is of type "{type(args[key])}" not {value}{NC}')
#         sys.exit(1)

# if any(type(i) != str for i in args['variables']):
#     print('All items in "variables" must be strings')
#     sys.exit(1)

# module_name = args['name']
# eq = args['equation']
# integer_bits = args['integer_bits']
# fractional_bits = args['fractional_bits']
# variables = args['variables']
# out_variable = args['out_variable']
# lower_bound, upper_bound = args['lower_bound'], args['upper_bound']
# tolerance = args['tolerance']

eq = '(x+((y*(z+2))+(3*(x*2))))' # should be inputtable from sys argv
integer_bits = 16 # should be inputtable from sys argv
fractional_bits = 16

add_module = lambda n, a, b, c: f'add adder{n} ( {a}, {b}, {c} );'
mult_module = lambda n, a, b, c: f'mult multiplier{n} ( {a}, {b}, {c} );'
div_module = lambda n, a, b, c: f'div divider{n} ( {a}, {b}, {c} );'

func_modules = {
    '+' : add_module, 
    '*' : mult_module,
    '/' : div_module,
}

module_types = {
    '+' : 'adder',
    '*' : 'mult',
    '/' : 'div',
}

def module_type_length(modules, module_type):
    return len([i for i in modules if module_type in i]) + 1

def get_operator(string):
    if '+' in i:
        return '+'
    elif '*' in i:
        return '*'
    elif '/' in i:
        return '/'

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

def convert_decimals(string):
    if re.match(r'^-*(\d|\.)+$', string):
        return f"{integer_bits}'b{decimal_to_fixed_point(float(string), integer_bits, fractional_bits)}"
    else: 
        return string

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
    # level = [i for i in parsed if i[0] == max_depth-1]
    level = [i for i in parsed if i[0] == n]

    for _, i in level:
        pre_replacement = i
        intermediates[i] = f'term{len(intermediates)+1}'

        for _, key in parsed:
            if key in i and i != key:
                print('here', i)
                i = i.replace(key, intermediates[key])
                print('after', i)

        op = get_operator(key)

        first, second = i.split(op)
        first = first.strip('()')
        second = second.strip('()')
        first, second = [convert_decimals(i) for i in (first, second)]

        update_modules(modules, op, first, second, intermediates[pre_replacement], pre_replacement)


print(modules)
print(intermediates)

variables = ['x', 'y', 'z'] # should be inputtable from sys argv
out_variable = 'out'
module_name = 'eq'

last_term_key = list(intermediates.keys())[-1]
last_term = intermediates[last_term_key]
del intermediates[last_term_key]
modules = [i if last_term not in i else i.replace(last_term, out_variable) for i in modules]

module_variables = ",\n\t".join(["input [N-1:0] " + i for i in variables])
include_string = '`include "../ops.sv"\n\n'
module_header = f'module {module_name} #(\n\tparameter N={integer_bits},\n\tparameter Q={fractional_bits}\n)(\n\t{module_variables},\n\toutput [N-1:0] {out_variable} \n);\n\t'
intermediates_string = 'reg [N-1:0] ' + ', '.join(intermediates.values()) + ';\n\n\t'
modules_string = '\n\t'.join(modules)
verilog_file = include_string + module_header + intermediates_string + modules_string + '\nendmodule'
print(verilog_file)
# print([i.group() for i in re.finditer('-*(\d|\.)+', verilog_file)])

# last intermediate value should be overwritten with out_variable

lower_bound, upper_bound = (-31, 31)
tolerance = 1e-2

generate_random_vars = '\n\t'.join(f'{i} = np.random.randint(lower_bound, upper_bound)' for i in variables)
generate_binary_values = '\n\t'.join(f'binary_{i} = decimal_to_fixed_point({i}, int_bits, frac_bits)' for i in variables)
generate_seting_values = '\n\t'.join(f'dut.{i}.value = BinaryValue(binary_{i})' for i in variables)

test_file = f'''import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.binary import BinaryValue
from models import fixed_point_to_decimal, decimal_to_fixed_point
from models import check_with_tolerance
import numpy as np


@cocotb.test()
async def exp_test(dut):
    int_bits = {integer_bits}
    frac_bits = {fractional_bits}
    lower_bound, upper_bound = {lower_bound}, {upper_bound}
    tolerance = 

    for i in range(100):
        {generate_random_vars}

        {generate_binary_values}    
        {generate_seting_values}

        await Timer(2, units="ns")

        output_value = fixed_point_to_decimal(str(dut.{out_variable}.value), int_bits, frac_bits)
        actual = {eq} # unprocessed equation

        assert check_with_tolerance(
            actual,
            output_value, 
            {tolerance}
        )
'''

print(test_file)

makefile = f'''
# defaults
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
