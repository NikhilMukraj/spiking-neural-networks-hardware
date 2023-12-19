import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import check_with_tolerance
import numpy as np


async def generate_clock(dut):
    for cycle in range(100):
        dut.clk.value = 0
        await Timer(4, units="ns")
        dut.clk.value = 1
        await Timer(4, units="ns")

@cocotb.test()
async def test(dut):
    await cocotb.start(generate_clock(dut))
    
    int_bits = 16
    frac_bits = 16
    tolerance = 0.1

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
    apply = 0
    rst = 1

    dut.i.value = BinaryValue(decimal_to_fixed_point(i, int_bits, frac_bits))
    dut.v_init.value = BinaryValue(decimal_to_fixed_point(v_init, int_bits, frac_bits))
    dut.w_init.value = BinaryValue(decimal_to_fixed_point(w_init, int_bits, frac_bits))
    dut.v_th.value = BinaryValue(decimal_to_fixed_point(v_th, int_bits, frac_bits))
    dut.dt.value = BinaryValue(decimal_to_fixed_point(dt, int_bits, frac_bits))
    dut.t.value = BinaryValue(decimal_to_fixed_point(t, int_bits, frac_bits))
    dut.a.value = BinaryValue(decimal_to_fixed_point(a, int_bits, frac_bits))
    dut.b.value = BinaryValue(decimal_to_fixed_point(b, int_bits, frac_bits))
    dut.c.value = BinaryValue(decimal_to_fixed_point(c, int_bits, frac_bits))
    dut.d.value = BinaryValue(decimal_to_fixed_point(d, int_bits, frac_bits))

    dut.rst.value = BinaryValue(str(rst))
    await RisingEdge(dut.clk) 

    rst = 0
    dut.rst.value = BinaryValue(str(rst))
    await RisingEdge(dut.clk) 

    for _ in range(5):
        apply = 1
        dut.apply.value = BinaryValue(str(apply))
        dut._log.info(f'apply: {dut.apply.value}')
        await RisingEdge(dut.clk) 

        output_voltage = fixed_point_to_decimal(str(dut.voltage.value), int_bits, frac_bits)
        output_w = fixed_point_to_decimal(str(dut.w.value), int_bits, frac_bits)
        output_dv = fixed_point_to_decimal(str(dut.dv.value), int_bits, frac_bits)
        output_dw = fixed_point_to_decimal(str(dut.dw.value), int_bits, frac_bits)
        output_new_voltage = fixed_point_to_decimal(str(dut.new_voltage.value), int_bits, frac_bits)
        output_new_w = fixed_point_to_decimal(str(dut.new_w.value), int_bits, frac_bits)
        rst_value = str(dut.rst.value)

        dut._log.info(f'voltage: {output_voltage}')
        dut._log.info(f'w: {output_w}')
        dut._log.info(f'dv: {output_dv}')
        dut._log.info(f'dw: {output_dw}')
        dut._log.info(f'new v: {output_new_voltage}')
        dut._log.info(f'new w: {output_new_w}')
        dut._log.info(f'rst value: {rst_value}')
        dut._log.info(f'eq: {dut.eq.value}')
        dut._log.info(f'gt: {dut.gt.value}')

        apply = 0
        dut.apply.value = BinaryValue(str(apply))
        dut._log.info(f'apply: {dut.apply.value}')
        await RisingEdge(dut.clk) 
