if __name__ == '__main__':
    from arithmetic_of_GF import *
    from value_witness import *
else:
    from task3.arithmetic_of_GF import *
    from task3.value_witness import *


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
        k = k_start
        qr = list()

        while k > j_start:
            r, j = primes[k], j_start
            while j < k:
                q = primes[j]
                if q * r <= max_qr:
                    qr.append([q, r])
                    j += 1
                else:
                    break
            k -= 1

        i_start, j_start = j_start, j_start + 1
        if qr:
            list_pqr_append([p, qr])

    return list_pqr


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
    start_time = time.time()

    list_pqr = find_list_pqr_primes(n)
    end_time_pqr = time.time()
    print('find list pqr, time {:.3f}.'.format(end_time_pqr - start_time))

    start_time_dict = time.time()
    primes_1 = (psnp.primes(2, n // (2 * 3)) - 1).tolist()
    pool = mp.Pool()
    map_div = pool.map_async(find_set_division, primes_1)
    pool.close()
    pool.join()
    global div_dict
    div_dict = {
        primes_1[i]: div for i, div in zip(range(len(primes_1)), map_div.get())
    }
    end_time_dict = time.time()
    print(
        'div_dict init, time {:.3f}.'.format(end_time_dict - start_time_dict)
    )

    ratios = [
        find_ratio_for_pqr(pqr[0], qr) for pqr in list_pqr for qr in pqr[1]
    ]

    if len(ratios) != 0:
        ratio = np.sum(ratios, dtype=float) / len(ratios)
        end_time = time.time()
        print('Время расчета {:.3f}(с.).'.format(end_time - start_time))
        print(ratio)
    else:
        print("Количество n=pqr равно 0!")


if __name__ == '__main__':
    main()
