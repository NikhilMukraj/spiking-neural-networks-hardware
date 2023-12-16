import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import adder_model, check_with_tolerance
import numpy as np


@cocotb.test()
async def exp_test(dut):
    int_bits = 16
    frac_bits = 16
    lower_bound = 1
    upper_bound = 10

    for i in range(100):
        x = np.random.randint(lower_bound, upper_bound)

        binary_x = decimal_to_fixed_point(x, int_bits, frac_bits)    
        dut.x.value = BinaryValue(binary_x)

        await Timer(2, units="ns")

        output = str(dut.out.value)
        assert 'x' not in output, f'{x} | {output}'
        output_value = fixed_point_to_decimal(output, int_bits, frac_bits)

        actual = np.exp(x)

        assert check_with_tolerance(
            actual,
            output_value, 
            1
        ), f'{x} | {actual} | {output_value}'
