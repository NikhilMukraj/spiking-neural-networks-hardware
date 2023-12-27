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

    bit_string = '10101010'

    for i in bit_string:
        dut.miso.value = BinaryValue(str(i))
        dut._log.info(f'input value: {dut.miso.value}')
        await RisingEdge(dut.clk) 

    assert str(dut.led.value) == bit_string, f'{str(dut.led.value)} != {bit_string}'
