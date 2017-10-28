import time
if __name__ == '__main__':
    from arithmetic_of_GF import *
    from value_witness import *
else:
    from task3.arithmetic_of_GF import *
    from task3.value_witness import *
from collections import deque


def find_list_pqr_primes(n):
    primes = tuple(get_list_primes(n // (2 * 3)))
    i_start, j_start, k_start = 0, 1, len(primes) - 1

    list_p, qr, index_end = list(), deque(), 0
    list_p_append, qr_append = list_p.append, qr.append
    while k_start - i_start > 2:
        p = primes[i_start]
        max_qr = n // p
        while primes[j_start] * primes[k_start] > max_qr:
            k_start -= 1
        k = k_start

        while k > j_start:
            r, j = primes[k], j_start
            while j < k:
                q = primes[j]
                if q * r <= max_qr:
                    qr_append([q, r])
                    index_end += 1
                    j += 1
                else:
                    break
            k -= 1

        i_start, j_start = j_start, j_start + 1
        list_p_append([p, index_end])

    return list_p, qr


def find_D_dict_bin_set(Di):
    set_bin, Di_dict = set(), dict()
    for d in Di:
        bin_d = find_bin_of_number(d)
        if bin_d in set_bin:
            Di_dict.get(bin_d).add(d)
        else:
            Di_dict.update({bin_d: {d}})
            set_bin.add(bin_d)

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
    qr_1, pr_1, pq_1 = q * r - 1, p * r - 1, p * q - 1

    Dp = {i for i in div_dict.get(p - 1) if qr_1 % i == 0}
    Dq = {i for i in div_dict.get(q - 1) if pr_1 % i == 0}
    Dr = {i for i in div_dict.get(r - 1) if i <= pq_1 and pq_1 % i == 0}

    Dp_dict = find_D_dict_bin_set(Dp)
    Dq_dict = find_D_dict_bin_set(Dq)
    Dr_dict = find_D_dict_bin_set(Dr)

    key_iter = range(min(len(Dp_dict), len(Dp_dict), len(Dq_dict)))
    E = zip(
        find_E(Dp_dict, key_iter),
        find_E(Dq_dict, key_iter),
        find_E(Dr_dict, key_iter)
    )
    nw = 0
    for e in E:
        nw += e[0] * e[1] * e[2]

    return nw


def find_ratio_for_pqr(p, qr, div_dict):
    q, r = qr[0], qr[1]
    return find_number_witness_pqr(p, q, r, div_dict) / (p * q * r)


def main():
    n = int(input(['Введите N: ']))
    start_time = time.time()

    list_p, list_qr = find_list_pqr_primes(n)
    start_time_dict = time.time()
    primes = get_list_primes(n // (2 * 3))
    div_dict = dict.fromkeys([i - 1 for i in primes])
    div_dict = {(i - 1): find_set_division(i - 1) for i in primes}
    primes.clear()
    end_time_dict = time.time()
    print('div_dict init with time {:.3f}.'.format(end_time_dict - start_time_dict))
    ratios, n = list(), 0

    for pi in list_p:
        p, i_end = pi[0], pi[1]
        while n < i_end:
            qr, n = list_qr.popleft(), n + 1
            ratio = find_ratio_for_pqr(p, qr, div_dict)
            ratios.append(ratio)

    if n != 0:
        ratio = np.sum(ratios, dtype=float) / n
        end_time = time.time()
        print('{:.3f}.'.format(end_time - start_time))
        print(ratio)
    else:
        print("Количество n=pqr равно 0!")


if __name__ == '__main__':
    main()
