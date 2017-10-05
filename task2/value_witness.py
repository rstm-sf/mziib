import sys
sys.path.append("../task1/")
from arithmetic_of_GF import *


def find_set_division(n):
    div_set = {i for i in range(2, n) if n % i == 0}
    return div_set | {1, n}


def find_bin_of_number(n):
    bin_n, _ = find_bin_and_remainder_for_number(n)
    return bin_n


def find_number_witness_pq(p, q):
    Dp, Dq = find_set_division(p - 1), find_set_division(q - 1)
    D = Dp & Dq

    bins_D_dict = {d: find_bin_of_number(d) for d in D}
    bins_D_set = set(bins_D_dict.values())
    Di = {i: set() for i in bins_D_set}
    for d in D:
        Di.get(bins_D_dict[d]).add(d)

    nw = 0
    for i in bins_D_set:
        s_i = 0
        for d in Di.get(i):
            s_i += function_Euler(d)
        nw += s_i * s_i

    return nw


print(find_number_witness_pq(11, 31))
