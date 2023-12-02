import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import adder_model, check_with_tolerance
import numpy as np


@cocotb.test()
async def adder_test(dut):
    int_bits = 16
    frac_bits = 16
    bounds = 100

    for i in range(100):
        a = np.random.uniform(-bounds, bounds)
        b = np.random.uniform(-bounds, bounds)
       
        # converting to right precision
        a = fixed_point_to_decimal(decimal_to_fixed_point(a, int_bits, frac_bits), int_bits, frac_bits)
        b = fixed_point_to_decimal(decimal_to_fixed_point(b, int_bits, frac_bits), int_bits, frac_bits)

        result = adder_model(a, b, int_bits)

        dut.a.value = BinaryValue(decimal_to_fixed_point(a, int_bits, frac_bits))
        dut.b.value = BinaryValue(decimal_to_fixed_point(b, int_bits, frac_bits))

        await Timer(2, units="ns")

        output = fixed_point_to_decimal(str(dut.c.value), int_bits, frac_bits)

        assert check_with_tolerance(output, result, 1e-3), \
        f'{i} : {output} != {a} + {b}'
