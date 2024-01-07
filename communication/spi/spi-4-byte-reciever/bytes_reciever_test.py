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

async def test_bit_string_recieve(dut, bit_string):
    dut._log.info('-' * 30)
    for step, i in enumerate(bit_string):
        # await FallingEdge(dut.sck) 
        dut.ss.value = BinaryValue(str('0'))
        dut.apply.value = BinaryValue(str('1'))
        dut.mosi.value = BinaryValue(str(i))
        await FallingEdge(dut.sck) 
        dut._log.info(f'{step} | input value: {dut.mosi.value}')
        dut._log.info(f'{step} | temp_out value: {dut.temp_out.value}')
        dut._log.info(f'{step} | bytes_count value: {dut.bytes_count.value}')
        dut._log.info(f'{step} | done_bytes value: {dut.done_bytes.value}')

    assert str(dut.out.value) == bit_string and str(dut.done_bytes.value) == '1', \
    f'{str(dut.out.value)} != {bit_string}'

@cocotb.test()
async def spi_peripheral_test(dut):
    await cocotb.start(generate_clock(dut, 100))
    await cocotb.start(generate_spi_clock(dut, 100))

    dut.rst.value = BinaryValue(str(1))
    dut.ss.value = BinaryValue(str(1))
    await RisingEdge(dut.sck) 

    dut.rst.value = BinaryValue(str(0))
    await RisingEdge(dut.sck) 

    dut.mosi.value = BinaryValue(str(1))
    await FallingEdge(dut.sck) 

    await test_bit_string_recieve(dut, '10101010111100000000111101010101')
