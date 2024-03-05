# fit ae^tx to linear piecewise functions, at split = -0.5 and 0.5
# reduce range of t change to -1 to 1, beyond t change of -200 to 200 is capped or parameterizable
# range reduction by division or lookup of msb
# after fitting, seperate a and t functions may not be necessary

import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import check_with_tolerance
import numpy as np


async def generate_clock(dut, timesteps):
    for cycle in range(timesteps):
        dut.clk.value = 0
        await Timer(4, units='ns')
        dut.clk.value = 1
        await Timer(4, units='ns')

get_slope = lambda func, a, b: (func(a) - func(b)) / (a - b)
get_intercept = lambda func, x, m: func(x) - m * x

# assume symmetric weight change function
def get_slope_and_intercept(a, tau):
    exp = lambda x: a * np.exp(x * tau)

    m1 = get_slope(exp, -1, -0.5) 
    m2 = get_slope(exp, -0.5, 0)
    b1 = get_intercept(exp, -0.5, m1)
    b2 = get_intercept(exp, 0, m2) 

    return m1, m2, b1, b2

correct_precision = lambda x: fixed_point_to_decimal(decimal_to_fixed_point(x, int_bits, frac_bits), int_bits, frac_bits)
to_binary = lambda x:  BinaryValue(decimal_to_fixed_point(x, int_bits, frac_bits))

def get_weight(t_change, a_plus, a_minus, tau_plus, tau_minus):
    if t_change > 0:
        return a_plus * np.exp(np.abs(t_change * tau_plus) * -1)
    else:
        return -1 * a_minus * np.exp(np.abs(t_change * tau_minus) * -1)

@cocotb.test()
async def stdp_test(dut):
    int_bits = 16
    frac_bits = 16

    a = tau = 1

    m1, m2, b1, b2 = [correct_precision(i) for i in get_slope_and_intercept(a, tau)]
    
    dut.m1.value = to_binary(m1)
    dut.m2.value = to_binary(m2)
    dut.b1.value = to_binary(b1)
    dut.b2.value = to_binary(b2)

    timesteps = 100

    await cocotb.start(generate_clock(dut, timesteps * 2 + 20))

    for i in range(timesteps):
        t_change = np.random.uniform(-1, 1)        

        dut.t_change.value = to_binary(t_change)
        dut.apply.value = BinaryValue(1)

        await RisingEdge(dut.clk) 

        out = fixed_point_to_decimal(str(dut.dw.value), int_bits, frac_bits)
        expected = get_weight(t_change, a, a, tau, tau)

        assert check_with_tolerance(output, expected, 1e-3)
        