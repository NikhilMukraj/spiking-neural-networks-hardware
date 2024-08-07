# https://www.geeksforgeeks.org/computer-organization-booths-algorithm/
# implement booth mulitplier in python and then in hardware
from fixed_point_models import fixed_point_to_decimal, decimal_to_fixed_point
import logging
import sys
import numpy as np
import json
from tqdm import tqdm


def bit_add(m: str, n: str, length: int):
    lmax = max(len(m), len(n))
    c = 0
    ml = [0] * (lmax - len(m)) + [int(x) for x in list(m)]
    nl = [0] * (lmax - len(n)) + [int(x) for x in list(n)]
    rl = []
    for i in range(1, lmax+1):
        if ml[-i] + nl[-i] + c == 0:
            rl.insert(0, 0)
            c = 0
        elif ml[-i] + nl[-i] + c == 1:
            rl.insert(0, 1)
            c = 0
        elif ml[-i] + nl[-i] + c == 2:
            rl.insert(0, 0)
            c = 1
        elif ml[-i] + nl[-i] + c == 3:
            rl.insert(0, 1)
            c = 1
    if c == 1:
        rl.insert(0, 1)
    if length > len(rl):
        rl = [0] * (length - len(rl)) + rl
    else:
        rl = rl[-length:]
    rl = ''.join([str(x) for x in rl])
    return rl

def two_comp(n: str) -> str:
    l = list(n)
    for i in range(len(l)):
        l[i] = '0' if l[i] == '1' else '1'
    return bit_add(''.join(l), ('0' * (len(l) - 1)) + '1', len(l))

# right arithmetic shift
def bit_shift(n: str, shift: int) -> str:
    if shift > 0:
        if n[0] == '0':
            n_ = ''.join(['0'] * shift) + n
        else:
            n_ = ''.join(['1'] * shift) + n
        return n_[:len(n)]
    else:
        n_ = n + ''.join(['0'] * (-shift))
        return n_[-len(n):]

def booth_algo(m: int, r: int, int_bits: int, frac_bits: int=0, debug: bool=False) -> dict:
    if debug:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(message)s')
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')

    # if frac_bits != 0 and frac_bits != int_bits:
    #     raise NotImplementedError('Currently only implemented for balanced integer and fractional bits and integers')

    m_string = decimal_to_fixed_point(m, int_bits, frac_bits)
    r_string = decimal_to_fixed_point(r, int_bits, frac_bits)
    
    length = int_bits + frac_bits

    # ilen = length + length + 1 # The common length of internal variables
    a = m_string + '0' * (length + 1) # A: place M in leftmost position. Fill the left bits with 0.
    s = two_comp(m_string) + '0' * (length + 1) # S: place negative M in leftmost position.
    p = '0' * (length) + r_string + '0' # P: place R by rightmost 0.

    logging.debug('Internal variables:')
    logging.debug(f'M = {m}')
    logging.debug(f'R = {r}')
    logging.debug(f'A = {a}')
    logging.debug(f'S = {s}')
    logging.debug(f'P = {p}')

    p_init = p
    ops = []
    iterations = []

    for i in range(length):
        logging.debug(f'Step {i+1}:')

        op = p[-2:]
        ops.append(op)

        logging.debug(f'\tThe last 2 bits of p are: {"".join(op)}')
        if op == '10':
            logging.debug('\tP = (P+S) >> 1')
            p = bit_add(p, s, len(p))
        elif op == '01':
            logging.debug('\tP = (P+A) >> 1')
            p = bit_add(p, a, len(p))
        elif op == '00':
            logging.debug('\tP = P >> 1')
        elif op == '11':
            logging.debug('\tP = P >> 1')

        iterations.append(p)

        p = bit_shift(p, 1)
        logging.debug(f'\tP = {p}\n')

    iterations.append(p)

    # answer_string = p[0] + p[-length:-1]

    answer_string = p[0] + p[int_bits + 1:int_bits + length]
    answer = fixed_point_to_decimal(answer_string, int_bits, frac_bits)

    logging.debug(f'The answer is: {p}, {answer}')
    logging.debug(f'Verification: {m} * {r} = {m * r}')
    logging.debug(f'Verification: {m_string} * {r_string} = {answer_string}')

    return {
        'm' : m,
        'r' : r,
        'm_string' : m_string,
        'r_string' : r_string,
        'two_comp_m' : two_comp(m_string),
        'a' : a,
        's' : s,
        'p_init' : p_init,
        'ops' : ops,
        'iterations' : iterations,
        'answer' : answer,
        'answer_string' : answer_string,
    }

def find_substring(a, b, int_bits, frac_bits, use_integer=False):
    a = fixed_point_to_decimal(decimal_to_fixed_point(a, int_bits, frac_bits), int_bits, frac_bits)
    b = fixed_point_to_decimal(decimal_to_fixed_point(b, int_bits, frac_bits), int_bits, frac_bits)

    c = a * b
    c_string = decimal_to_fixed_point(c, int_bits, frac_bits)

    output = booth_algo(a, b, int_bits=int_bits, frac_bits=frac_bits)

    # ignore sign for now
    if use_integer:
        c_string = c_string[0] + c_string[1:int_bits]
    
    index = output['iterations'][-1].find(c_string[1:])

    if index == -1:
        return [output['iterations'][-1], f'{c_string} not found', output['answer_string'], output['answer'], c, output['answer'] == c ]
    else:
        return [output['iterations'][-1], index, output['answer_string'], output['answer'], c, output['answer'] == c]

substrings = {}
for int_bits, frac_bits in tqdm([(16, 16), (8, 8), (4, 8), (12, 8)]):
    for i in range(100):
        a = np.random.uniform(-16, 16)
        b = np.random.uniform(-16, 16)

        output = find_substring(a, b, int_bits, frac_bits, True)
        if str((int_bits, frac_bits)) not in substrings:
            a_dict = {'a' : {'num' : a, 'string' : decimal_to_fixed_point(a, int_bits, frac_bits)}}
            b_dict = {'b' : {'num' : b, 'string' : decimal_to_fixed_point(b, int_bits, frac_bits)}}

            substrings[str((int_bits, frac_bits))] = [{f'nums_{i+1}' : [a_dict, b_dict], 'output' : output}]
        else:
            substrings[str((int_bits, frac_bits))].append([{f'nums_{i+1}' : [a_dict, b_dict], 'output' : output}])

with open('booth_substrings.json', 'w+') as f: 
    json.dump(substrings, f, indent=4)

# try prescaling by multplying by 2 ** frac_bits first and using booth algo with int_bits=(int_bits+frac_bits)
