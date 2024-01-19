# https://github.com/alexforencich/cocotbext-axi

# https://www.chipverify.com/verilog/verilog-single-port-ram
# https://github.com/ChloeeeYoo/Verilog_simplemodule/blob/main/01.Memory/ram.v
# https://alchitry.com/sdram-verilog contains ram_test tb
# use ram test tb from cocotb 

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

@cocotb.test
def ram_model_test(dut):
    await generate_clock(dut, 100)

    raise NotImplementedError("Example unfinished")
