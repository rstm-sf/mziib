import multiprocessing as mp
import matplotlib.pyplot as plt
if __name__ == '__main__':
    import sys
    sys.path.append("../")
from task1.arithmetic_of_GF import *


def find_set_division(n):
    div_set = {1, n}

    if n != 1 and n not in primes_frozenset:
        p, div_set_pow2 = 1, set()
        while is_even(n):
            n, p = n // 2, p * 2
            div_set.add(n)
            div_set_pow2.add(p)
        div_set |= div_set_pow2

        if n == 1 or n in primes_frozenset:
            return div_set

        div_set2 = {i for i in range(3, n // 3 + 1, 2) if n % i == 0}
        div_set |= div_set2 | {i * j for i in div_set_pow2 for j in div_set2}

    return div_set


def find_bin_of_number(n):
    bin_n, _ = find_bin_and_remainder_for_number(n)
    return bin_n


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


def find_number_witness_pq(p, q):
    n1, n2 = (q - 1, p - 1) if p > q else (p - 1, q - 1)
    D = {i for i in find_set_division(n1) if n2 % i == 0}

    Di_dict = find_D_dict_bin_set(D)

    nw = 0
    for set_d in Di_dict.values():
        s_i = 0
        for d in set_d:
            s_i += function_Euler(d)
        nw += s_i * s_i

    return nw


def find_list_pairs_primes(n, primes=None):
    if primes is None:
        primes = tuple(psnp.primes(2, n // 2).tolist())
        return find_list_pairs_primes(n, primes)
    pairs, start, end = list(), 0, len(primes) - 1

    while end > start:
        q, i = primes[end], start
        while i < end:
            p = primes[i]
            if p * q <= n:
                pairs.append([p, q])
                i += 1
            else:
                break
        end -= 1

    return pairs


def find_ratio_for_pair(pq):
    p, q = pq[0], pq[1]
    return find_number_witness_pq(p, q) / (p * q)


def find_ratio_for_number(n):
    pairs = find_list_pairs_primes(n)

    if len(pairs) > 2600:
        pool = mp.Pool()
        result = [pool.map_async(find_ratio_for_pair, pairs)]
        pool.close()
        pool.join()
        return np.sum([p.get() for p in result]) / len(pairs)
    else:
        return np.sum(find_ratio_for_pair(pq) for pq in pairs) / len(pairs)


def calc_for_one_number():
    print('Введите число: n =', end=' ')
    n = int(input())

    start_time = time.time()
    ratio = find_ratio_for_number(n)
    end_time = time.time()

    print('=' * 80)
    print("Среднее отношение:\t{}".format(ratio))
    print("Время расчета (c.):\t{:.3f}".format(end_time - start_time))
    print('=' * 80)


def init_n_list_and_filename_pdf():
    print(
        "Выберете вариант промежутка для графика чисел N\n",
        "1: N = [1e+2, 1e+4];\n",
        "2: N = [1e+4, 1e+6];\n",
        "3: N = [1e+6, 1e+7]."
    )
    print("Вариант: ", end='')
    x_mod = int(input())

    if x_mod == 1:
        n_list = [i * 100 for i in range(1, 101)]
        filename_pdf = "plot_of_1e2_1e4.pdf"
    elif x_mod == 2:
        n_list = [i * 10000 for i in range(1, 11)]
        n_list.extend([i * 100000 for i in range(1, 11)])
        filename_pdf = "plot_of_1e4_1e6.pdf"
    elif x_mod == 3:
        n_list = [i * 1000000 for i in range(1, 11)]
        filename_pdf = "plot_of_1e6_1e7.pdf"
    else:
        print("Ошибка ввода!")
        n_list, filename_pdf = None, None

    return n_list, filename_pdf


def find_ratios_for_n_list(n_list):
    st = time.time()
    ratios = [find_ratio_for_number(i) for i in n_list]
    et = time.time()
    print("Время расчета для n=pq (c.):  \t{:.3f}".format(et - st))

    return ratios


def main(*args):
    n_list, filename_pdf = args
    if n_list is None or filename_pdf is None:
        return

    mp.freeze_support()

    f = plt.figure()
    plt.style.use('ggplot')
    plt.title(
        "Cреднее отношение числа свидетелей к числу\n" +
        "для полупростых чисел $n$ меньших $N$"
    )
    plt.xlabel(r'$N$')
    plt.ylabel('Среднее отношение')
    plt.plot(n_list, find_ratios_for_n_list(n_list), label=r'$n=pq$')
    plt.legend()
    plt.show()
    f.savefig(filename_pdf, bbox_inches='tight')


if __name__ == '__main__':
    main(*init_n_list_and_filename_pdf())
