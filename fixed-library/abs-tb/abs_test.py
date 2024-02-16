import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import adder_model, check_with_tolerance
import numpy as np


@cocotb.test()
async def abs_test(dut):
    int_bits = 16
    frac_bits = 16
    lower_bound = -100
    upper_bound = 100

    for i in range(100):
        x = np.random.uniform(lower_bound, upper_bound)
       
        x = fixed_point_to_decimal(decimal_to_fixed_point(x, int_bits, frac_bits), int_bits, frac_bits)
        
        dut.x.value = BinaryValue(decimal_to_fixed_point(x, int_bits, frac_bits))

        await Timer(2, units="ns")

        output = fixed_point_to_decimal(str(dut.x.value), int_bits, frac_bits)
        result = np.abs(x)

        assert check_with_tolerance(output, result, 1e-3), \
        f'{i} : {output} != |{x}|'
