import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import check_with_tolerance
import numpy as np


async def test_negator(a, dut, int_bits, frac_bits):
    result = a * -1

    dut.a.value = BinaryValue(decimal_to_fixed_point(a, int_bits, frac_bits))

    await Timer(2, units="ns")

    output = fixed_point_to_decimal(str(dut.out.value), int_bits, frac_bits)

    result_bits = decimal_to_fixed_point(result, 16, 16)

    assert check_with_tolerance(output, result, 1e-3), \
    f'''{i} : {output} != -1 * {a} | {result} |
    {str(dut.out.value)} vs {result_bits} from {str(dut.a.value)}'''

@cocotb.test()
async def negator_test(dut):
    int_bits = -16
    frac_bits = 16
    lower_bound = -128
    upper_bound = 128

    for i in range(100):
        a = np.random.uniform(lower_bound, upper_bound)
        a = fixed_point_to_decimal(decimal_to_fixed_point(a, int_bits, frac_bits), int_bits, frac_bits)

        await test_negator(a, dut, int_bits, frac_bits)

    a = 0
    a = fixed_point_to_decimal(decimal_to_fixed_point(a, int_bits, frac_bits), int_bits, frac_bits)

    await test_negator(a, dut, int_bits, frac_bits)
