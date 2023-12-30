import cocotb
from cocotb.triggers import FallingEdge, RisingEdge, Timer
from cocotb.binary import BinaryValue
import numpy as np


async def generate_clock(dut, timesteps):
    for cycle in range(timesteps):
        dut.clk.value = 0
        await Timer(4, units='ns')
        dut.clk.value = 1
        await Timer(4, units='ns')

# if always (*) is replaced with always (posedge clk) and 
# timer for sck is not a multiple of clk,
# bits are shifted in
async def generate_spi_clock(dut, timesteps):
    for cycle in range(timesteps):
        dut.sck.value = 0
        await Timer(4, units='ns')
        dut.sck.value = 1
        await Timer(4, units='ns')

@cocotb.test()
async def spi_peripheral_test(dut):
    await cocotb.start(generate_clock(dut, 100))
    await cocotb.start(generate_spi_clock(dut, 100))

    dut.rst.value = BinaryValue(str('1'))
    dut.ss.value = BinaryValue(str('1'))
    await RisingEdge(dut.sck) 

    dut.rst.value = BinaryValue(str('0'))
    await RisingEdge(dut.sck) 

    # dut.ss.value = BinaryValue(str('0'))
    dut.mosi.value = BinaryValue(str('1'))
    await FallingEdge(dut.sck) 

    # dut._log.info(f'select value: {dut.ss.value}')
    # dut._log.info(f'data value: {dut.data.value}')
    # await FallingEdge(dut.sck) 

    bit_string = '10101010'

    for step, i in enumerate(bit_string):
        # await FallingEdge(dut.sck) 
        dut.ss.value = BinaryValue(str('0'))
        dut.mosi.value = BinaryValue(str(i))
        await FallingEdge(dut.sck) 
        dut._log.info(f'{step} | input value: {dut.mosi.value}')
        dut._log.info(f'{step} | data value: {dut.data.value}')
        dut._log.info(f'{step} | count value: {dut.bit_count.value}')
        dut._log.info(f'{step} | done value: {dut.done.value}')

    assert str(dut.dout.value) == bit_string and str(dut.done.value) == '1', \
    f'{str(dut.dout.value)} != {bit_string}'
