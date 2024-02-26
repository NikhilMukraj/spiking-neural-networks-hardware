import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import check_with_tolerance
import numpy as np


@cocotb.test()
async def piecewise_test(dut):
    int_bits = 16
    frac_bits = 16
    lower_bound = -128
    upper_bound = 128

    for i in range(100):
        x = np.random.uniform(lower_bound, upper_bound)
        m1 = np.random.uniform(lower_bound, upper_bound)
        m2 = np.random.uniform(lower_bound, upper_bound)
        b1 = np.random.uniform(lower_bound, upper_bound)
        b2 = np.random.uniform(lower_bound, upper_bound)
        split = np.random.uniform(lower_bound, upper_bound)

        binary_x = decimal_to_fixed_point(x, int_bits, frac_bits)    
        dut.x.value = BinaryValue(binary_x)

        await Timer(2, units="ns")

        output = str(dut.out.value)
        assert 'x' not in output, f'x: {x} | output: {output}'
        output_value = fixed_point_to_decimal(output, int_bits, frac_bits)

        actual = m1 * x + b1 if x < split else m2 * x + b2

        dut._log.info(dut.two_power.value)

        assert check_with_tolerance(
            actual,
            output_value, 
            1
        ), f'''x: {x} | expected: {actual} | result: {output_value} | binary: {dut.out.value}''' 
