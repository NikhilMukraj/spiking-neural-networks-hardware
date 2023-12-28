import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.binary import BinaryValue
import numpy as np


async def generate_clock(dut, timesteps):
    for cycle in range(timesteps):
        dut.clk.value = 0
        await Timer(4, units='ns')
        dut.clk.value = 1
        await Timer(4, units='ns')

@cocotb.test()
async def spi_peripheral_test(dut):
    await cocotb.start(generate_clock(dut, 100))
    # redo this but start sck and clk clocks
    # wait for dut.sck

    dut.rst.value = BinaryValue(str('1'))
    await RisingEdge(dut.clk) 

    dut.rst.value = BinaryValue(str('0'))
    await RisingEdge(dut.clk) 

    dut.ss.value = BinaryValue(str('0'))
    dut.miso.value = BinaryValue(str('1'))
    await RisingEdge(dut.clk) 

    bit_string = '10101010'

    for i in bit_string:
        await RisingEdge(dut.clk) 
        dut.miso.value = BinaryValue(str(i))
        dut._log.info(f'input value: {dut.miso.value}')
        await RisingEdge(dut.clk) 

    assert str(dut.led.value) == bit_string, f'{str(dut.led.value)} != {bit_string}'
