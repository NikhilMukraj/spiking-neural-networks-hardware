import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import check_with_tolerance
import numpy as np


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

        binary_i = decimal_to_fixed_point(i, int_bits, frac_bits)
        binary_v_init = decimal_to_fixed_point(v_init, int_bits, frac_bits)
        binary_w_init = decimal_to_fixed_point(w_init, int_bits, frac_bits)    
        binary_v_th = decimal_to_fixed_point(v_th, int_bits, frac_bits)
        binary_dt = decimal_to_fixed_point(dt, int_bits, frac_bits)
        binary_t = decimal_to_fixed_point(t, int_bits, frac_bits)
        binary_a = decimal_to_fixed_point(a, int_bits, frac_bits)
        binary_b = decimal_to_fixed_point(b, int_bits, frac_bits)
        binary_c = decimal_to_fixed_point(c, int_bits, frac_bits)
        binary_d = decimal_to_fixed_point(d, int_bits, frac_bits)
        binary_apply = decimal_to_fixed_point(apply, 1, 0)
        dut.i.value = BinaryValue(binary_x)
        dut.v_init.value = BinaryValue(binary_y)
        dut.v_th.value = BinaryValue(binary_vth)
        dut.dt.value = BinaryValue(binary_dt)
        dut.t.value = BinaryValue(binary_t)
        dut.a.value = BinaryValue(binary_a)
        dut.b.value = BinaryValue(binary_b)
        dut.c.value = BinaryValue(binary_c)
        dut.d.value = BinaryValue(binary_d)

        for i in range(5):
            dut.apply.value = BinaryValue(binary_apply)
            await Timer(2, units="ns")

            output_voltage = fixed_point_to_decimal(str(dut.voltage.value), int_bits, frac_bits)
            output_w = fixed_point_to_decimal(str(dut.w.value), int_bits, frac_bits)

            dut._log.info(f'voltge: {output_voltage}')
            dut._log.info(f'w: {output_w}')

            apply = 0
            binary_apply = decimal_to_fixed_point(apply, 1, 0)
            
            dut.apply.value = BinaryValue(2, units="ns")
            await Timer(2, units="ns")
