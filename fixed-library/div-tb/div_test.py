import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import adder_model, check_with_tolerance
import numpy as np


@cocotb.test()
async def reciprocal(dut):
    int_bits = 16
    frac_bits = 16
    bounds = 128

    for i in range(100):
        a = np.random.randint(-bounds, bounds)
        b = np.random.randint(-bounds, bounds)
        if b == 0:
            b = 1

        binary_a = decimal_to_fixed_point(a, int_bits, frac_bits) 
        binary_b = decimal_to_fixed_point(b, int_bits, frac_bits)    
        dut.a.value = BinaryValue(binary_a)
        dut.b.value = BinaryValue(binary_b)

        await Timer(20, units="ns")

        output = str(dut.c.value)
        output_value = fixed_point_to_decimal(output, int_bits, frac_bits)

        assert check_with_tolerance(
            a / b,
            output_value, 
            1e-1
        )
        assert ((a / b >= 0) and (output_value >= 0)) \
            or ((a / b < 0) and (output_value < 0))
