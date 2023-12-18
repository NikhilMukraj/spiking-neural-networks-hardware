import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import check_with_tolerance
import numpy as np


convert_to_binary = lambda x, integer_bits, fractional_bits : decimal_to_fixed_point(x, integer_bits, fractional_bits)

@cocotb.test()
async def test(dut):
    int_bits = 16
    frac_bits = 16
    tolerance = 0.1

    for i in range(100):
        i = 40
        v_init = -55
        w_init = 30
        v_th = 30
        dt = 0.5
        t = 0.1 # here tau_m is 1/tau_m to not have to divide
        # later replace dt * t with just a "step" variable
        a = 0.01
        b = 0.25
        c = -55
        d = 8.0
        apply = 1
        rst = 1

        dut.i.value = BinaryValue(convert_to_binary(i, int_bits, frac_bits))
        dut.v_init.value = BinaryValue(convert_to_binary(v_init, int_bits, frac_bits))
        dut.v_th.value = BinaryValue(convert_to_binary(v_th, int_bits, frac_bits))
        dut.dt.value = BinaryValue(convert_to_binary(dt, int_bits, frac_bits))
        dut.t.value = BinaryValue(convert_to_binary(t, int_bits, frac_bits))
        dut.a.value = BinaryValue(convert_to_binary(a, int_bits, frac_bits))
        dut.b.value = BinaryValue(convert_to_binary(b, int_bits, frac_bits))
        dut.c.value = BinaryValue(convert_to_binary(c, int_bits, frac_bits))
        dut.d.value = BinaryValue(convert_to_binary(d, int_bits, frac_bits))

        dut.rst.value = BinaryValue(str(rst))
        await Timer(2, units="ns")

        rst = 0
        dut.rst.value(str(rst))
        await Timer(2, units="ns")

        for i in range(5):
            dut.apply.value = BinaryValue(str(apply))
            await Timer(2, units="ns")

            output_voltage = fixed_point_to_decimal(str(dut.voltage.value), int_bits, frac_bits)
            output_w = fixed_point_to_decimal(str(dut.w.value), int_bits, frac_bits)

            dut._log.info(f'voltge: {output_voltage}')
            dut._log.info(f'w: {output_w}')

            apply = 0
            dut.apply.value = BinaryValue(str(apply), units="ns")
            await Timer(2, units="ns")
