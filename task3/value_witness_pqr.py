if __name__ == '__main__':
    import sys
    sys.path.append("../")
from task1.arithmetic_of_GF import *
from task2.value_witness import *


div_dict = dict()


def find_list_pqr_primes(n):
    primes = tuple(psnp.primes(2, n // (2 * 3)).tolist())
    i_start, j_start, k_start = 0, 1, len(primes) - 1

    list_pqr = list()
    list_pqr_append = list_pqr.append
    while k_start - i_start > 2:
        p = primes[i_start]
        max_qr = n // p
        while primes[j_start] * primes[k_start] > max_qr:
            k_start -= 1

        qr = find_list_pairs_primes(max_qr, primes[j_start:k_start + 1])
        if qr:
            list_pqr_append([p, qr])
        i_start, j_start = j_start, j_start + 1

    return list_pqr


def find_E(D_dict, key_iter):
    E = list()
    for key in key_iter:
        s = 0
        for d in D_dict.get(key):
            s += function_Euler(d)
        E.append(s)

    return E


def find_number_witness_pqr(p, q, r):
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


def find_ratio_for_pqr(p, qr):
    q, r = qr[0], qr[1]
    return find_number_witness_pqr(p, q, r) / (p * q * r)


def main():
    n = int(input(['Введите N: ']))
    st1 = time.time()

    list_pqr = find_list_pqr_primes(n)
    et2 = time.time()
    print('Сгенерированы тройки за время {:.3f} (с.)'.format(et2 - st1))

    st3 = time.time()
    primes_1 = (psnp.primes(2, n // (2 * 3)) - 1).tolist()
    pool = mp.Pool()
    map_div = pool.map_async(find_set_division, primes_1)
    pool.close()
    pool.join()
    global div_dict
    div_dict = {
        primes_1[i]: div for i, div in zip(range(len(primes_1)), map_div.get())
    }
    et3 = time.time()
    print(
        'Сгенерирован словарь делителей за время {:.3f} (с.)'.format(et3 - st3)
    )

    ratios = [
        find_ratio_for_pqr(pqr[0], qr) for pqr in list_pqr for qr in pqr[1]
    ]

    if len(ratios) != 0:
        ratio = np.sum(ratios, dtype=float) / len(ratios)
        et1 = time.time()
        print('Время расчета {:.3f} (с.)'.format(et1 - st1))
        print(ratio)
    else:
        print("Количество n=pqr равно 0!")


if __name__ == '__main__':
    main()
