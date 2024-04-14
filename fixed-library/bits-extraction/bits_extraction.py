# ignore sign for now
# for booth multplier, find (in code simulation) where desired bit string is
# find pattern among the indices
# for mult module, find (in hardware simulation) where desired bit string is
# find pattern among the indices

def find_substring(a, b, out_string, int_bits, frac_bits):
    a = fixed_point_to_decimal(decimal_to_fixed_point(a, int_bits, frac_bits))
    b = fixed_point_to_decimal(decimal_to_fixed_point(b, int_bits, frac_bits))

    c = a * b
    c_string = decimal_to_fixed_point(c_string, int_bits, frac_bits)

    return out_string.find(c_string[1:]) # return match