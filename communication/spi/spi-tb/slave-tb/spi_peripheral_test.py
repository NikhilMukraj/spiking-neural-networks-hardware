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
    await RisingEdge(dut.sck) 

    dut.rst.value = BinaryValue(str('0'))
    await RisingEdge(dut.sck) 

    dut.ss.value = BinaryValue(str('0'))
    dut.mosi.value = BinaryValue(str('1'))
    await RisingEdge(dut.sck) 

    dut._log.info(f'select value: {dut.ss.value}')
    dut._log.info(f'select_d value: {dut.ss_d.value}')
    await RisingEdge(dut.sck) 

    bit_string = '10101010'

    for i in bit_string:
        # await RisingEdge(dut.clk) 
        dut.mosi.value = BinaryValue(str(i))
        dut._log.info(f'input value: {dut.mosi.value}')
        dut._log.info(f'data_q value: {dut.data_q.value}')
        dut._log.info(f'sck_q value: {dut.sck_q.value}')
        dut._log.info(f'sck_d value: {dut.sck_d.value}')
        dut._log.info(f'sck value: {dut.sck.value}')
        await RisingEdge(dut.sck) 

    assert str(dut.dout.value) == bit_string, f'{str(dut.dout.value)} != {bit_string}'
