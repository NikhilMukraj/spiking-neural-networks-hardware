import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import multiplier_model, check_with_tolerance
import numpy as np


async def generate_clock(dut, timesteps):
    for cycle in range(timesteps):
        dut.clk.value = 0
        await Timer(4, units='ns')
        dut.clk.value = 1
        await Timer(4, units='ns')

@cocotb.test()
async def operation_test(dut):
    int_bits = 16
    frac_bits = 16
    stack_length = 5
    stack_bits = np.ceil(np.log2(stack_length))

    generate_clock(dut, 100)

    dut.rst = BinaryValue(1)

    await RisingEdge(dut.clk) 
    await RisingEdge(dut.clk) 

    # test loading values

    dut.rst.value = BinaryValue(0)

    a = decimal_to_fixed_point(3, int_bits, frac_bits)
    b = decimal_to_fixed_point(2, int_bits, frac_bits)

    index1 = decimal_to_fixed_point(0, stack_bits, 0)
    index2 = decimal_to_fixed_point(1, stack_bits, 0)

    dut.value = a
    dut.index1 = index1
    dut.operand = BinaryValue('001')

    await RisingEdge(dut.clk) 

    dut._log.info(str(dut.stack.value))

    dut.value = b
    dut.index2 = index2
    dut.operand = BinaryValue('010')

    await RisingEdge(dut.clk) 

    dut._log.info(str(dut.stack.value))

    # test operation
