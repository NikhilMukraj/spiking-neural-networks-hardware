# check if all internal variables are correct
# test reseting with rst and then doing next multiplication
import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import booth_algo, check_with_tolerance
import numpy as np


async def generate_clock(dut, timesteps):
    for cycle in range(timesteps):
        dut.clk.value = 0
        await Timer(4, units='ns')
        dut.clk.value = 1
        await Timer(4, units='ns')

@cocotb.test()
async def booth_mult_test(dut):
    int_bits = 16
    frac_bits = 16
    lower_bound = -128
    upper_bound = 128

    dut.rst.value = 1

    for i in range(100):
        a = np.random.uniform(lower_bound, upper_bound)
        b = np.random.uniform(lower_bound, upper_bound)

        booth_verification = booth_algo(a, b, length=int_bits + frac_bits)

        # fixing precision
        a = fixed_point_to_decimal(decimal_to_fixed_point(a, int_bits, frac_bits), int_bits, frac_bits)
        b = fixed_point_to_decimal(decimal_to_fixed_point(b, int_bits, frac_bits), int_bits, frac_bits)

        dut.a.value = decimal_to_fixed_point(a, int_bits, frac_bits)
        dut.b.value = decimal_to_fixed_point(b, int_bits, frac_bits)

        await RisingEdge(dut.clk)

        assert dut.a_static.value == booth_verification['a']
        assert dut.s.value == booth_verification['s']
        assert dut.p_init.value == booth_verification['p_init']
        assert dut.two_comp_m.value == booth_verification['two_comp_m']
