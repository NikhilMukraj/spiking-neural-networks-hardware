import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
import numpy as np


async def generate_clock(dut, timesteps):
    for cycle in range(timesteps):
        dut.clk.value = 0
        await Timer(4, units='ns')
        dut.clk.value = 1
        await Timer(4, units='ns')

@cocotb.test()
async def pn_gen_test(dut):
    generate_clock(dut, 120)

    dut.seed = decimal_to_fixed_point(1, 32, 0)
    dut.rst = BinaryValue(1)

    await RisingEdge(dut.clk)
    dut.next = BinaryValue(1)
    await RisingEdge(dut.clk)
    
    nums = []
    for i in range(100):
        nums.append(dut.num.value)

        await RisingEdge(dut.clk)
    
    with open('output.log') as f:
        for i in nums:
            f.write(f'{i}\n')
    