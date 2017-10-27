import time
if __name__ == '__main__':
    from arithmetic_of_GF import *
    from value_witness import *
else:
    from task3.arithmetic_of_GF import *
    from task3.value_witness import *


def find_list_pqr_primes(n):
    primes, pqr = get_list_primes(n // (2 * 3)), list()

    while len(primes) > 2:
        r, primes_2 = primes.pop(), primes.copy()
        while len(primes_2) > 1:
            q = primes_2.pop()
            for i in primes:
                if i * q <= n // r:
                    pqr.append([i, q, r])
                else:
                    break

    return pqr


def find_D_dict_bin_set(Di):
    bins_Di_dict = {d: find_bin_of_number(d) for d in Di}
    Di_dict = {i: set() for i in set(bins_Di_dict.values())}
    for d in Di:
        Di_dict.get(bins_Di_dict[d]).add(d)

    return Di_dict


def find_E(D_dict, key_iter):
    E = list()
    for key in key_iter:
        s = 0
        for d in D_dict.get(key):
            s += function_Euler(d)
        E.append(s)

    return E


def find_number_witness_pqr(p, q, r, div_dict):
    qr, pr, pq = q * r - 1, p * r - 1, p * q - 1
    get_set_div = div_dict.get
    if get_set_div(p - 1) is None:
        div_dict[p - 1] = find_set_division(p - 1)
    if get_set_div(q - 1) is None:
        div_dict[q - 1] = find_set_division(q - 1)
    if get_set_div(r - 1) is None:
        div_dict[r - 1] = find_set_division(r - 1)

    Dp = {i for i in get_set_div(p - 1) if qr % i == 0}
    Dq = {i for i in get_set_div(q - 1) if pr % i == 0}
    Dr = {i for i in get_set_div(r - 1) if pq % i == 0}

    Dp_dict = find_D_dict_bin_set(Dp)
    Dq_dict = find_D_dict_bin_set(Dq)
    Dr_dict = find_D_dict_bin_set(Dr)

    key_iter = set(Dp_dict.keys()) & set(Dq_dict.keys()) & set(Dr_dict.keys())
    E = zip(
        find_E(Dp_dict, key_iter),
        find_E(Dq_dict, key_iter),
        find_E(Dr_dict, key_iter)
    )
    nw = 0
    for e in E:
        nw += e[0] * e[1] * e[2]

    return nw


def find_ratio_for_pqr(pqr, div_dict):
    p, q, r = pqr[0], pqr[1], pqr[2]
    return find_number_witness_pqr(p, q, r, div_dict) / (p * q * r)


if __name__ == '__main__':
    n = int(input(['Введите N: ']))
    pqr = find_list_pqr_primes(n)
    primes = get_list_primes(n)
    div_dict = dict.fromkeys([i - 1 for i in primes])
    ratios = np.sum(find_ratio_for_pqr(i, div_dict) for i in pqr) / len(pqr)
    print(ratios)
