import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.binary import BinaryValue
from models import fixed_point_to_decimal, decimal_to_fixed_point
from models import check_with_tolerance
import numpy as np


@cocotb.test()
async def reciprocal(dut):
    int_bits = 16
    frac_bits = 16
    # bounds = 2 ** 15
    bounds = 128

    with open('test.txt', 'w+') as f: f.write('')

    for i in range(100):
        a = np.random.randint(-bounds, bounds)
        if a == 0:
            a = 1

        binary_a = decimal_to_fixed_point(a, int_bits, frac_bits)    
        dut.a.value = BinaryValue(binary_a)

        await Timer(2, units="ns")

        output = str(dut.out.value)
        output_value = fixed_point_to_decimal(output, int_bits, frac_bits)

        # with open('t.txt', 'w+') as f: f.write(f'{1 / a} | {output} | {output_value}')
        with open('test.txt', 'a+') as f: f.write(f'{a} | {1 / a} | {output} | {output_value}\n')

        assert check_with_tolerance(
            1 / a,
            output_value, 
            1e-3
        )
