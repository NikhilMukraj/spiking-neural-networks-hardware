# check if all internal variables are correct
# test reseting with rst and then doing next multiplication
import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.binary import BinaryValue
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
from fixed_point_models import booth_algo, check_with_tolerance
import numpy as np


async def generate_clock(dut, timesteps):
    for cycle in range(timesteps):
        dut.clk.value = 0
        await Timer(4, units='ns')
        dut.clk.value = 1
        await Timer(4, units='ns')

@cocotb.test()
async def booth_mult_test(dut):
    int_bits = 4
    frac_bits = 4
    lower_bound = -3
    upper_bound = 3

    iterations = 100
    await cocotb.start(generate_clock(dut, iterations * (int_bits + frac_bits + 8)))

    dut.rst.value = 1
    dut.enable.value = 0
    await RisingEdge(dut.clk)

    dut.rst.value = 1
    await RisingEdge(dut.clk)

    for i in range(iterations):
        a = np.random.uniform(lower_bound, upper_bound)
        b = np.random.uniform(lower_bound, upper_bound)

        # fixing precision
        a = fixed_point_to_decimal(decimal_to_fixed_point(a, int_bits, frac_bits), int_bits, frac_bits)
        b = fixed_point_to_decimal(decimal_to_fixed_point(b, int_bits, frac_bits), int_bits, frac_bits)

        binary_a = decimal_to_fixed_point(a, int_bits, frac_bits)
        binary_b = decimal_to_fixed_point(b, int_bits, frac_bits)

        dut.a.value = BinaryValue(binary_a)
        dut.b.value = BinaryValue(binary_b)

        booth_verification = booth_algo(a, b, int_bits=int_bits, frac_bits=frac_bits)

        assert binary_a == booth_verification['m_string'], \
        f"{binary_a} != {booth_verification['m_string']}"
        assert binary_b == booth_verification['r_string'], \
        f"{binary_b} != {booth_verification['r_string']}"

        dut._log.info(f'a: {binary_a} | b: {binary_b}')

        # on the last iteration only check the relevant bits in the c wire
        # on the last iteration, account for negative 
        # (booth_verification['iterations'][-1][0] + booth_verification['iterations'][-1][int_bits + frac_bits:])
        # could adapt algo to account for sign in last output

        # when this is done test p_new = p + 1'b1

        await RisingEdge(dut.clk)

        # if below fails, print these values to debug
        # if below fails because static values have not been set yet, wait 1 clock cycle to set values

        # modify p init to work correctly

        # ****** CHECK IF NUMBER ADDED TO ~a IS THE SAME IN BOOTH ALGO AS WELL ******
        # ****** CALCULATE WHERE VALID ANSWER IS BASED ON THE NUMBER OF INT AND FRAC BITS ******
        # ****** DETERMINE IF THAT CALCULATION HOLDS TRUE FOR MANY POSSIBLE VALUES ******

        # check if two comp m is the same if only dealing with integer or after modifying to work with fractionals

        assert str(dut.p_init.value) == booth_verification['p_init'], \
        f"{dut.p_init.value} != {booth_verification['p_init']}" 
        # assert str(dut.two_comp_m.value) == booth_verification['two_comp_m'], \
        # f"{dut.two_comp_m.value} != {booth_verification['two_comp_m']}"
        # assert str(dut.a_static.value) == booth_verification['a'], \
        # f"{dut.a_static.value} != {booth_verification['a']}"
        # assert str(dut.s.value) == booth_verification['s'], \
        # f"{dut.s.value} != {booth_verification['s']}"

        dut.enable.value = BinaryValue(1)
        await RisingEdge(dut.clk)

        index = 0
        while dut.done.value != 1:
            dut._log.info(f'count: {dut.count.value}, max_count: {dut.max_count.value}')
            dut._log.info(f'p: {dut.p.value}')
            dut._log.info(f'p_new: {dut.p_new.value}')
            dut._log.info(f'iteration[{index}]: {booth_verification["iterations"][index]}')

            # assert fixed_point_to_decimal(str(dut.count.value), int(np.ceil(np.log2(a))), 0) == index, \
            # f"{dut.count.value} != {index}"

            # assert dut.p.value == booth_verification['iterations'][index], \
            # f"{dut.p.value} != {booth_verification['iterations'][index]}"

            # assert dut.op.value == booth_verification['iterations'][index][-2:], \
            # f"{dut.op.value} != {booth_verification['iterations'][index][-2:]}"

            await RisingEdge(dut.clk)

            index += 1

        dut._log.info(f'c: {dut.c.value}')
        assert dut.c.value == booth_verification['answer_string'], \
        f"{dut.c.value} != {booth_verification['answer_string']}"

        numeric_answer = fixed_point_to_decimal(dut.c.value, int_bits, frac_bits)
        assert numeric_answer == booth_verification['answer'], \
        f"{numeric_answer} != {booth_verification['answer']}"

        # dut.rst.value = 1
        await RisingEdge(dut.clk)
