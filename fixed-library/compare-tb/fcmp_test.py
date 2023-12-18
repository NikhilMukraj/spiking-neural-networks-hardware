import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import adder_model, check_with_tolerance
import numpy as np


@cocotb.test()
async def fcmp_test(dut):
    int_bits = 16
    frac_bits = 16
    bounds = 5

    for i in range(100):
        a = np.random.randint(-bounds, bounds)
        b = np.random.randint(-bounds, bounds)
        # a = np.random.randint(0, bounds)
        # b = np.random.randint(0, bounds)

        dut.a.value = BinaryValue(decimal_to_fixed_point(a, int_bits, frac_bits))
        dut.b.value = BinaryValue(decimal_to_fixed_point(b, int_bits, frac_bits))

        await Timer(2, units="ns")

        gt = dut.gt.value
        lt = dut.lt.value
        eq = dut.eq.value

        log_string = f'gt : {gt} | lt : {lt} | eq : {eq} | a : {a}, b : {b}'
        dut._log.info(log_string)

        if a > b:
            assert str(lt) == '0'
            assert str(gt) == '1'
            assert str(eq) == '0'
        elif a < b:
            assert str(lt) == '1'
            assert str(gt) == '0'
            assert str(eq) == '0'
        else:
            assert str(lt) == '0'
            assert str(gt) == '0'
            assert str(eq) == '1'