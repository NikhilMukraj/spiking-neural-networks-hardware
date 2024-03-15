import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import check_with_tolerance
import numpy as np


async def generate_clock(dut, timesteps):
    for cycle in range(timesteps):
        dut.clk.value = 0
        await Timer(4, units='ns')
        dut.clk.value = 1
        await Timer(4, units='ns')

# make sure weight changes align with actual stdp

@cocotb.test()
async def coupled_test(dut):
    i = 40
    v_init = -65
    w_init = 30
    v_th = 30
    step = 0.5 / 10 # dt / tau_m
    a = 0.01
    b = 0.25
    c = -55
    d = 8.0
    apply = 0
    rst = 1

    dut.i.value = BinaryValue(decimal_to_fixed_point(i, int_bits, frac_bits))
    dut.v_init.value = BinaryValue(decimal_to_fixed_point(v_init, int_bits, frac_bits))
    dut.w_init.value = BinaryValue(decimal_to_fixed_point(w_init, int_bits, frac_bits))
    dut.v_th.value = BinaryValue(decimal_to_fixed_point(v_th, int_bits, frac_bits))
    dut.step.value = BinaryValue(decimal_to_fixed_point(step, int_bits, frac_bits))
    dut.a.value = BinaryValue(decimal_to_fixed_point(a, int_bits, frac_bits))
    dut.b.value = BinaryValue(decimal_to_fixed_point(b, int_bits, frac_bits))
    dut.c.value = BinaryValue(decimal_to_fixed_point(c, int_bits, frac_bits))
    dut.d.value = BinaryValue(decimal_to_fixed_point(d, int_bits, frac_bits))

    dut.dt_reciprocal.value = BinaryValue(decimal_to_fixed_point(1 / dt, int_bits, frac_bits))
    dut.cm_reciprocal.value = BinaryValue(decimal_to_fixed_point(1, int_bits, frac_bits))
