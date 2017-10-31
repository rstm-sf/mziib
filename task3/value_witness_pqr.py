if __name__ == '__main__':
    import sys
    sys.path.append("../")
from itertools import repeat
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
    Dr = {i for i in div_dict.get(r - 1) if pq_1 % i == 0}

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


def find_ratio_for_number_pqr(n):
    list_pqr = find_list_pqr_primes(n)

    primes_1 = (psnp.primes(2, n // (2 * 3)) - 1).tolist()
    if len(div_dict) < len(primes_1):
        init_div_dict(n, primes_1)

    ratios = list()
    for pqr in list_pqr:
        p, qr_list = pqr[0], pqr[1]
        if len(qr_list) > 2000:
            pool = mp.Pool()
            result = pool.starmap_async(
                find_ratio_for_pqr, zip(repeat(p), qr_list)
            )
            pool.close()
            pool.join()
            ratios.extend(result.get())
        else:
            ratios.extend([find_ratio_for_pqr(p, qr) for qr in qr_list])

    if len(ratios) != 0:
        return np.sum(ratios, dtype=float) / len(ratios)
    else:
        print("Количество n=pqr равно 0!")
        return -1


def init_div_dict(n, primes_1=None):
    if primes_1 is None:
        primes_1 = (psnp.primes(2, n // (2 * 3)) - 1).tolist()
    pool = mp.Pool()
    map_div = pool.map_async(find_set_division, primes_1)
    pool.close()
    pool.join()
    global div_dict
    div_dict = {
        primes_1[i]: div
        for i, div in zip(range(len(primes_1)), map_div.get())
    }


def find_ratios_for_n_list_pqr(n_list):
    st = time.time()
    ratios = [find_ratio_for_number_pqr(i) for i in n_list]
    et = time.time()
    print("Время расчета для n=pqr (c.):  \t{:.3f}".format(et - st))

    return ratios


def main_pqr(*args):
    n_list, filename_pdf = args
    if n_list is None or filename_pdf is None:
        return

    mp.freeze_support()
    init_div_dict(n_list[len(n_list) - 1])

    f = plt.figure()
    plt.style.use('ggplot')
    plt.title(
        "Cреднее отношение числа свидетелей к числу\n" +
        "для составных чисел $n$ меньших $N$"
    )
    plt.xlabel(r'$N$')
    plt.ylabel('Среднее отношение')
    plt.plot(n_list, find_ratios_for_n_list(n_list), label=r'$n=pq$')
    plt.plot(n_list, find_ratios_for_n_list_pqr(n_list), label=r'$n=pqr$')
    plt.legend()
    plt.show()
    f.savefig(filename_pdf, bbox_inches='tight')


if __name__ == '__main__':
    main_pqr(*init_n_list_and_filename_pdf())
