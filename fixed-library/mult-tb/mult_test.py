import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import adder_model, check_with_tolerance
import numpy as np


@cocotb.test()
async def mult_test(dut):
    int_bits = 16
    frac_bits = 16
    lower_bound = -5
    upper_bound = 5

    for i in range(100):
        a = np.random.uniform(-lower_bound, upper_bound)
        b = np.random.uniform(-lower_bound, upper_bound)

        a = fixed_point_to_decimal(decimal_to_fixed_point(a, int_bits, frac_bits), int_bits, frac_bits)
        b = fixed_point_to_decimal(decimal_to_fixed_point(b, int_bits, frac_bits), int_bits, frac_bits)

        result = multiplier_model(a, b, int_bits - 1)

        dut.a.value = BinaryValue(decimal_to_fixed_point(a, int_bits, frac_bits))
        dut.b.value = BinaryValue(decimal_to_fixed_point(b, int_bits, frac_bits))

        await Timer(2, units="ns")

        output = fixed_point_to_decimal(str(dut.c.value), int_bits, frac_bits)

        assert check_with_tolerance(output, result, 1e-3), \
        f'{i} : {output} != {a} * {b} | {result}'
