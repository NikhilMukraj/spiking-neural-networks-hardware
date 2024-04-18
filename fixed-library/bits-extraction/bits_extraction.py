# ignore sign for now
# for booth multplier, find (in code simulation) where desired bit string is
# find pattern among the indices
# for mult module, find (in hardware simulation) where desired bit string is
# find pattern among the indices

import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import multiplier_model, check_with_tolerance
import json
import numpy as np


def find_substring(a, b, out_string, int_bits, frac_bits, only_integer=True):
    a = fixed_point_to_decimal(decimal_to_fixed_point(a, int_bits, frac_bits))
    b = fixed_point_to_decimal(decimal_to_fixed_point(b, int_bits, frac_bits))

    # c = multiplier_model(a, b, int_bits + frac_bits - 1) * (2 ** (-frac_bits))
    c = a * b
    c_string = decimal_to_fixed_point(c, int_bits, frac_bits)

    if only_integer:
        end_index = int_bits
    else:
        end_index = len('c_string')

    looking_for = c_string[1:end_index]

    return (looking_for, out_string.find(looking_for)) # return match


@cocotb.test()
async def mult_test(dut):
    int_bits = 16
    frac_bits = 16
    lower_bound = -5
    upper_bound = 5

    substrings = {}

    for i in range(100):
        a = np.random.uniform(lower_bound, upper_bound)
        b = np.random.uniform(lower_bound, upper_bound)

        a = fixed_point_to_decimal(decimal_to_fixed_point(a, int_bits, frac_bits), int_bits, frac_bits)
        b = fixed_point_to_decimal(decimal_to_fixed_point(b, int_bits, frac_bits), int_bits, frac_bits)

        # result = multiplier_model(a, b, int_bits + frac_bits - 1) * (2 ** (-frac_bits))
        result = a * b

        dut.a.value = BinaryValue(decimal_to_fixed_point(a, int_bits, frac_bits))
        dut.b.value = BinaryValue(decimal_to_fixed_point(b, int_bits, frac_bits))

        await Timer(2, units="ns")

        output = fixed_point_to_decimal(str(dut.c.value), int_bits, frac_bits)
        looking_for, index = find_substring(a, b, str(dut.c.value), int_bits, frac_bits, only_integer=True)

        substrings[f'{a} * {b}'] = {
            'string' : str(dut.c.value), 
            'index' : index, 
            'looking_for' : looking_for,
        }

    with open('mult_bits_extraction.json', 'w+') as f:
        json.dump(substrings, f, indent=4)
    
    # if doesnt work, try multiplying integers to find where bits are
    # final result would probably be start of that substring, and then 15 more bits (accounting for sign bit)
    