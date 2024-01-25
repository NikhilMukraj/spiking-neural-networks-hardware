import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue


@cocotb.test()
async def fpga_pins_test(dut):
    dut.rst_n.value = BinaryValue('0')
    await Timer(4, units='ns')
    assert str(dut.leds.value) == '00000000', str(dut.leds.value)

    dut.in1.value = BinaryValue('1')
    await Timer(4, units='ns')
    assert str(dut.leds.value) == '11110000', str(dut.leds.value)

    dut.in2.value = BinaryValue('1')
    await Timer(4, units='ns')
    assert str(dut.leds.value) == '11111111', str(dut.leds.value)

    dut.in1.value = BinaryValue('0')
    await Timer(4, units='ns')
    assert str(dut.leds.value) == '00001111', str(dut.leds.value)

    dut.in2.value = BinaryValue('0')
    await Timer(4, units='ns')
    assert str(dut.leds.value) == '00000000', str(dut.leds.value)
