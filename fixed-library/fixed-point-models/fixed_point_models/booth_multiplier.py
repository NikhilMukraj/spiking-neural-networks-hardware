# https://www.geeksforgeeks.org/computer-organization-booths-algorithm/
# implement booth mulitplier in python and then in hardware
from models import fixed_point_to_decimal, decimal_to_fixed_point


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

def booth_algo(m, r, length):
    m_string = decimal_to_fixed_point(m, length, 0)
    r_string = decimal_to_fixed_point(r, length, 0)

    ilen = length + length + 1 #The common length of internal variables
    a = m_string + '0' * (length + 1) #A: place M in leftmost position. Fill the left bits with 0.
    s = two_comp(m_string) + '0' * (length + 1) #S: place negative M in leftmost position.
    p = '0' * (length + 1) + r_string + '0' #P: place R by rightmost 0.

    print('Internal variables:')
    print(f'M = {m}')
    print(f'R = {r}')
    print(f'A = {a}')
    print(f'S = {s}')
    print(f'P = {p}')

    for i in range(length):   #Do operation length times
        print(f'Step {i+1}:')

        op = p[-2:]
        print(f'\tThe last 2 bits of p are: {"".join(op)}')
        if op == '10':
            print('\tP = (P+S) >> 1')
            p = bit_add(p, s, len(p))
        elif op == '01':
            print('\tP = (P+A) >> 1')
            p = bit_add(p, a, len(p))
        elif op == '00':
            print('\tP = P >> 1')
        elif op == '11':
            print('\tP = P >> 1')

        p = bit_shift(p, 1)
        print(f'\tP = {p}\n')

    p = p[:-1]
    print(f'The answer is: {p}, {fixed_point_to_decimal(p[-4:], length, 0)}')
    print(f'Verification: {m} * {r} = {m * r}')
    print(f'Verification: {m_string} * {r_string} = {p[-4:]}')

if __name__ == '__main__':
    booth_algo(3, 2, 4)
