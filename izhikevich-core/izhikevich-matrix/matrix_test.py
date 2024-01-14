import cocotb
from cocotb.triggers import FallingEdge, RisingEdge, Timer
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

@cocotb.test()
async def spi_peripheral_test(dut):
    int_bits = 16
    frac_bits = 16

    await cocotb.start(generate_clock(dut, 100))

    dut.data1.value = BinaryValue(decimal_to_fixed_point(1, 8, 0))
    dut.data2.value = BinaryValue(decimal_to_fixed_point(2, 8, 0))
    dut.data3.value = BinaryValue(decimal_to_fixed_point(3, 8, 0))
    dut.data4.value = BinaryValue(decimal_to_fixed_point(4, 8, 0))
    dut.on.value = BinaryValue('00')
    await RisingEdge(dut.clk) 

    dut.on1.value = BinaryValue('01')
    await RisingEdge(dut.clk) 

    assert check_with_tolerance(fixed_point_to_decimal(dut.data1.value, 8, 0), 1 + 2)

    dut.on2.value = BinaryValue('11')
    await RisingEdge(dut.clk) 

    assert check_with_tolerance(fixed_point_to_decimal(dut.data2.value, 8, 0), 2 + 4)
