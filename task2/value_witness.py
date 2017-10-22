import multiprocessing as mp
import matplotlib.pyplot as plt
import time
if __name__ == '__main__':
    from arithmetic_of_GF import *
else:
    from task2.arithmetic_of_GF import *


def function_f_for_pollard(x, n):
    return 1 if x == 0 or x == n else (x * x + 1) % n


def get_list_primes(n):
    list_primes = list()
    for p in primes_tuple:
        if p > n:
            break
        list_primes.append(p)
    return list_primes


def pollard_rho(n, iterations_count=100000):
    r = random.randint(1, n)
    x0, x1 = r, function_f_for_pollard(r, n)
    g, i = gcd(abs(x1 - x0), n), 0

    while (g == 1 or g == n) and i < iterations_count:
        x0 = function_f_for_pollard(x0, n)
        x1 = function_f_for_pollard(function_f_for_pollard(x1, n), n)
        g, i = gcd(abs(x1 - x0), n), i + 1

    return g


def find_set_division(n):
    div_set = {1, n}

    if n != 1 and n not in primes_frozenset:
        p, div_set_pow2 = 1, set()
        while is_even(n):
            n, p = n >> 1, p << 1
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


def find_number_witness_pq(p, q):
    n1, n2 = (q - 1, p - 1) if p > q else (p - 1, q - 1)
    D = {i for i in find_set_division(n1) if n2 % i == 0}

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


def find_list_pairs_primes(n):
    primes, pairs = get_list_primes(n // 2), list()

    while len(primes) > 1:
        p = primes.pop()
        for i in primes:
            if i * p <= n:
                pairs.append([i, p])
            else:
                break

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
    print("Время расчета (c):\t{:.3f}".format(end_time - start_time))
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
    start_time = time.time()
    ratios = [find_ratio_for_number(i) for i in n_list]
    end_time = time.time()
    print("Время расчета (c):  \t{:.3f}".format(end_time - start_time))

    return ratios


def main(*args):
    n_list, filename_pdf = args
    if n_list is None or filename_pdf is None:
        return

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
