import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.binary import BinaryValue
import sys
sys.path.append("..")
from models import fixed_point_to_decimal, decimal_to_fixed_point
from models import check_with_tolerance
import numpy as np


@cocotb.test()
async def exp_test(dut):
    int_bits = 16
    frac_bits = 16
    bounds = 31

    for i in range(100):
        x = np.random.randint(-bounds, bounds)

        binary_x = decimal_to_fixed_point(x, int_bits, frac_bits)    
        dut.x.value = BinaryValue(binary_x)

        await Timer(2, units="ns")

        output = str(dut.out.value)
        assert 'x' not in output, f'{x} | {output}'
        output_value = fixed_point_to_decimal(output, int_bits, frac_bits)

        taylor = lambda x : 1 + x + (x * x * 0.5) + (x * x * x * (1/6))

        if x >= 0:
            actual = taylor(x)
        else:
            actual = 1 / taylor(-x)

        assert check_with_tolerance(
            actual, # np.exp(x),
            output_value, 
            1
        ), f'{x} | {actual} | {output_value}'
