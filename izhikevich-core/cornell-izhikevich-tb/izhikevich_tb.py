import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
import os


async def generate_clock(dut, timesteps):
    for cycle in range(timesteps):
        dut.clk.value = 0
        await Timer(4, units='ns')
        dut.clk.value = 1
        await Timer(4, units='ns')

@cocotb.test()
async def test(dut):
    timesteps = 1000

    with open('output.log', 'w+') as f:
        f.write('voltage,w,is_spiking,bit_string\n')

    await cocotb.start(generate_clock(dut, timesteps * 2 + 20))
    
    int_bits = 2
    frac_bits = 16

    # can play around with these params
    i = 0.15
    v_init = -0.7
    u_init = -0.2
    v_th = 0.3
    c14 = 1.4
    a = 0.02
    b = 0.2
    c = -0.5
    d = 0.02
    apply = 0
    rst = 1

    dut.i.value = BinaryValue(decimal_to_fixed_point(i, int_bits, frac_bits))
    dut.v_init.value = BinaryValue(decimal_to_fixed_point(v_init, int_bits, frac_bits))
    dut.u_init.value = BinaryValue(decimal_to_fixed_point(u_init, int_bits, frac_bits))
    dut.v_th.value = BinaryValue(decimal_to_fixed_point(v_th, int_bits, frac_bits))
    dut.c14.value = BinaryValue(decimal_to_fixed_point(c14, int_bits, frac_bits))
    dut.a.value = BinaryValue(decimal_to_fixed_point(a, int_bits, frac_bits))
    dut.b.value = BinaryValue(decimal_to_fixed_point(b, int_bits, frac_bits))
    dut.c.value = BinaryValue(decimal_to_fixed_point(c, int_bits, frac_bits))
    dut.d.value = BinaryValue(decimal_to_fixed_point(d, int_bits, frac_bits))

    dut.rst.value = BinaryValue(str(rst))
    await RisingEdge(dut.clk) 

    rst = 0
    dut.rst.value = BinaryValue(str(rst))
    await RisingEdge(dut.clk) 

    for current_step in range(timesteps):
        apply = 1
        dut.apply.value = BinaryValue(str(apply))
        await RisingEdge(dut.clk) 

        with open('output.log', 'a+') as f:
            output_voltage = fixed_point_to_decimal(str(dut.voltage.value), int_bits, frac_bits)
            output_u = fixed_point_to_decimal(str(dut.u.value), int_bits, frac_bits)
            f.write(f'{output_voltage}, {output_u}, {dut.is_spiking.value}, {dut.voltage.value}\n')

        apply = 0
        dut.apply.value = BinaryValue(str(apply))
        await RisingEdge(dut.clk) 
