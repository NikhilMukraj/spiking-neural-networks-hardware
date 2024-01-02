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
        dut.mosi.value = BinaryValue(str(i))
        await FallingEdge(dut.sck) 
        dut._log.info(f'{step} | input value: {dut.mosi.value}')
        dut._log.info(f'{step} | data_rx value: {dut.data_rx.value}')
        dut._log.info(f'{step} | count_rx value: {dut.bit_count_rx.value}')
        dut._log.info(f'{step} | done_rx value: {dut.done_rx.value}')

    assert str(dut.dout.value) == bit_string and str(dut.done_rx.value) == '1', \
    f'{str(dut.dout.value)} != {bit_string}'

async def test_bit_string_transmit(dut, bit_string, buffer=''):
    dut._log.info('-' * 30)
    dut.din.value = BinaryValue(bit_string)
    transmitted_bits = []

    for step, i in enumerate(bit_string + buffer):
        # await FallingEdge(dut.sck) 
        dut.ss.value = BinaryValue(str('0'))
        await RisingEdge(dut.sck) 
        transmitted_bits.append(str(dut.miso.value))
        dut._log.info(f'{step} | output value: {dut.miso.value}')
        dut._log.info(f'{step} | transmitted_bits: {"".join(transmitted_bits).rjust(8, "x")}')
        dut._log.info(f'{step} | count_tx value: {dut.bit_count_tx.value}')
        dut._log.info(f'{step} | done_tx value: {dut.done_tx.value}')

    assert ''.join(transmitted_bits)[-8:] == bit_string and str(dut.done_tx.value) == '1', \
    f'{"".join(transmitted_bits)[-8:]} != {bit_string}'

@cocotb.test()
async def spi_peripheral_test(dut):
    await cocotb.start(generate_clock(dut, 100))
    await cocotb.start(generate_spi_clock(dut, 100))

    dut.rst.value = BinaryValue(str('1'))
    dut.ss.value = BinaryValue(str('1'))
    await RisingEdge(dut.sck) 

    dut.rst.value = BinaryValue(str('0'))
    await RisingEdge(dut.sck) 

    dut.mosi.value = BinaryValue(str('1'))
    await FallingEdge(dut.sck) 

    await test_bit_string_recieve(dut, '10101010')
    await test_bit_string_recieve(dut, '11110000')

    await test_bit_string_transmit(dut, '11110000', 'z')
    await test_bit_string_transmit(dut, '01010101')
    await test_bit_string_transmit(dut, '11110000')
