import struct
import numpy as np


def float_to_hex(float_value):
    packed_data = struct.pack('!f', float_value)
    hex_string = hex(struct.unpack('!I', packed_data)[0])
    hex_string = hex_string[2:]

    return hex_string

hex_to_float = lambda x: struct.unpack('!f', bytes.fromhex(x))[0]

def float_to_int(float_value):
    packed_data = struct.pack('!f', float_value)
    integer_value = struct.unpack('!I', packed_data)[0]
    
    return integer_value

def check_with_tolerance(expected: float, actual: float, tolerance=1e-5):
    return np.abs(expected - actual) < tolerance

def fixed_point_to_decimal(binary_str: str, integer_bits: int, fractional_bits: int):
    if integer_bits + fractional_bits <= 3: 
        raise NotImplementedError('Unimplemented for size of 3 and under')
        
    sign_bit = int(binary_str[0], 2)
    
    integer_part = int(binary_str[1:integer_bits], 2)
    fractional_part = int(binary_str[integer_bits:], 2) / (2 ** fractional_bits)
    
    result = (-1) ** sign_bit * (integer_part + fractional_part)
    return result

def decimal_to_fixed_point(number: float, integer_bits: float, fractional_bits: float):
    if integer_bits + fractional_bits <= 3: 
        raise NotImplementedError('Unimplemented for size of 3 and under')

    sign_bit = '1' if number < 0 else '0'
    
    integer_part = bin(abs(int(number)))[2:].zfill(integer_bits-1)
    if fractional_bits > 0:
        fractional_part = bin(int(abs((number - int(number)) * (2 ** fractional_bits))))[2:].zfill(fractional_bits)
    else:
        fractional_part = ''

    return sign_bit + integer_part + fractional_part

def adder_model(a: int, b: int, n_bits: int = 4) -> int:
    result = a + b
    if result > 0:
        return result % (2 ** (n_bits - 1))
    else:
        return result % (-2 ** n_bits)

def multiplier_model(a: int, b: int, n_bits: int = 4) -> int:
    result = a * b
    if result > 0:
        return result % (2 ** (n_bits - 1))
    else:
        return result % (-2 ** n_bits)

def divider_model(a: int, b: int, n_bits: int = 4) -> int:
    result = a // b
    if result > 0:
        return result % (2 ** (n_bits - 1))
    else:
        return result % (-2 ** n_bits)

def paraboloid(a: int, b: int, c: int, x: int, n_bits: int = 4) -> int:
    x_square = multiplier_model(x, x, n_bits=n_bits)
    a_term = multiplier_model(a, x_square, n_bits=n_bits)

    b_term = multiplier_model(b, x, n_bits=n_bits)

    a_b_term = adder_model(a_term, b_term, n_bits=n_bits)

    return adder_model(a_b_term, c, n_bits=n_bits)

def piecewise(a: int, b: int, c: int, x: int, n_bits: int = 4) -> int:
    if x > 0:
        return paraboloid(a, b, c, x, n_bits=n_bits)
    elif x < 0:
        return paraboloid(-1 * a, b, c, x, n_bits=n_bits)
    else:
        return paraboloid(0, b, c, x, n_bits=n_bits)
