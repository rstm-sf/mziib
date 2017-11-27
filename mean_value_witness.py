import math
import multiprocessing as mp
import random
import time

import matplotlib.pyplot as plt
import numpy as np
import primesieve.numpy as psnp

from itertools import repeat

# _n_max - верхняя граница генерируемых простых чисел
_n_max = None
# _primes_frozenset - неизменяемое множество простых чисел
_primes_frozenset = None
# _div_dict - словарь делителей чисел вида p-1, где p - простое
_div_dict = None


def _init_primes_to_n_max(n=None):
    '''Функция инициализации множества простых чисел глобальной видимости.

    Инициализируются _n_max и _primes_frozenset с помощью модуля primesieve
    (https://github.com/hickford/primesieve-python).
    '''
    global _n_max, _primes_frozenset
    if n is None:
        _n_max = int(1e7)
    else:
        print('Введите число максимальное N =', end=' ')
        _n_max = int(input())
    print("Генерация простых чисел до N={}...".format(_n_max))
    st = time.time()
    _primes_frozenset = frozenset(psnp.primes(2, _n_max))
    et = time.time()
    print("Простые числа сгенерированы за {:.3f} (с.)".format(et - st))


def _init_div_dict(n, primes_1=None):
    '''Функция инициализации словаря делителей чисел вида p-1.

    Инициализируется _div_dict для чисел вида p-1, p - простое число.
    '''
    if primes_1 is None:
        primes_1 = (psnp.primes(2, n // (2 * 3)) - 1).tolist()
    pool = mp.Pool()
    map_div = pool.map_async(find_set_division, primes_1)
    pool.close()
    pool.join()
    global _div_dict
    _div_dict = {
        primes_1[i]: div
        for i, div in zip(range(len(primes_1)), map_div.get())
    }


def find_bin_and_remainder_of_number(n):
    '''Функция возвращает значения s, t для выражения n=t*2^s.

    Прим.: битовые операции интерпретируются медленнее.
    '''
    s, t = 0, n
    while t % 2 == 0:
        s += 1
        t = t // 2
    return s, t


def find_bin_of_number(n):
    '''Функция возвращеает значение s в выражении n=t*2^s.
    '''
    bin_n, _ = find_bin_and_remainder_of_number(n)
    return bin_n


def function_Euler(n):
    '''Функция Эйлера возвращает число чисел меньших и взаимнопростых с n.

    Для вычисления используется формула с каноническим разложением числа.
    Прим.: интерпретатор сравнивает быстрее объекты одинакового типа.
    '''
    if n == 1:
        return 1
    if n in _primes_frozenset:
        return n - 1

    value, i = float(n), 2
    while i * i <= n:
        if n % i == 0:
            i_inv = 1 / i
            n *= i_inv
            while n % i == 0:
                n *= i_inv
            value *= 1.0 - i_inv
        i += 1.0
    if n > 1.0:
        value *= 1.0 - 1 / n

    return int(value)


def find_set_division(n):
    '''Функция возвращающая множество делителей числа.

    Алгоритм факторизует на степень двойки и нечетное число.
    Затем проверяет на простоту. Если число не простое, то производится поиск
    всех делителей до получившегося числа, с последующим перемножением их
    на степени двойки для нахождения оставшихся делителей.
    '''
    div_set = {1, n}

    if n != 1 and n not in _primes_frozenset:
        p, div_set_pow2 = 1, set()
        while n % 2 == 0:
            n, p = n // 2, p * 2
            div_set.add(n)
            div_set_pow2.add(p)
        div_set |= div_set_pow2

        if n == 1 or n in _primes_frozenset:
            return div_set

        div_set2 = {i for i in range(3, n // 3 + 1, 2) if n % i == 0}
        div_set |= div_set2 | {
            i * j for i in div_set_pow2 for j in div_set2}

    return div_set


def find_D_dict_bin_set(Di):
    '''Функция возвращаяющает словарь для степени двойки.

    Разибвается множество на числа с одинаковыми степенями двойки.
    '''
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
    '''Функция суммирует значения функции для класса.

    key_iter - указывает на те множества, что будут учавствовать в расчете.
    D_dict - множества делителей, содержащих одинаковую степень двойки.
    '''
    E = list()
    for key in key_iter:
        s = 0
        for d in D_dict.get(key):
            s += function_Euler(d)
        E.append(s)
    return E


def find_number_witness_pq(p, q):
    '''Функция возвращает число свидетелей для числа n=p*q.

    Выполняется поиск делителей для меньшего числа и оставляются те, что делят
    большее число. Затем делители разбиваются на множества с одинаковыми
    степенями двойки и вычисляется число свидетелей.
    '''
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


def find_number_witness_pqr(p, q, r):
    '''Функция возвращает число свидетелей для числа n=p*q*r.

    Выполняется поиск делителей для меньшего числа и оставляются те, что делят
    большее число. Затем классы множеств разбиваются на подмножества
    содержащих одинаковую степень двойки. После, ищется максимальная степень
    двойки, входящая во все классы, и создается вектор E для вычисления
    числа свидетелей.
    '''
    qr_1, pr_1, pq_1 = q * r - 1, p * r - 1, p * q - 1

    Dp = {i for i in _div_dict.get(p - 1) if qr_1 % i == 0}
    Dq = {i for i in _div_dict.get(q - 1) if pr_1 % i == 0}
    Dr = {i for i in _div_dict.get(r - 1) if pq_1 % i == 0}

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


def find_list_pairs_primes(n, primes=None):
    '''Функция возвращает список пар (p, q).

    Алгоритм использует кортеж из простых чисел до n/2 включительно.
    В начале, указывается на последний индекс и составляются все пары,
    удовлетворяющие условию p * q <= n. Затем, индекс, указывающий сдвигается
    влево и продолжается добавление пар, начиная сначала. И так далее...
    '''
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


def find_list_pqr_primes(n):
    '''Функция возвращает список из (p, список пар (q, r)).

    Алгоритм использует кортеж из простых чисел до n/(2*3) включительно.
    В начале, "исключается" элемент под первым индексом и происходит
    поиск списка пар (q, r) с помощью функции find_list_pairs_primes.
    Затем сдивагается первый элемент вправо и снова выполняется поиск (q, r).
    И так далее...
    '''
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


def find_ratio_of_pair(pq):
    '''Функция возвращает отношение числа свидетелей числа к самому числу
    вида n=p*q.
    '''
    p, q = pq
    return find_number_witness_pq(p, q) / (p * q)


def find_ratio_for_pqr(p, qr):
    '''Функция возвращает отношение числа свидетелей числа к самому числу
    вида n=p*q*r.
    '''
    q, r = qr
    return find_number_witness_pqr(p, q, r) / (p * q * r)


def find_ratio_of_number_pairs(n):
    '''Функция возвращаетя среднее отношение числа свидетелей к числу вида
    вида n=p*q.

    Прим.: до какого-то момента использование map_async замедляет программу.
    '''
    pairs = find_list_pairs_primes(n)
    if len(pairs) > 2600:
        pool = mp.Pool()
        result = [pool.map_async(find_ratio_of_pair, pairs)]
        pool.close()
        pool.join()
        return np.sum([p.get() for p in result]) / len(pairs)
    else:
        return np.sum(find_ratio_of_pair(pq) for pq in pairs) / len(pairs)


def find_ratio_of_number_pqr(n):
    '''Функция возвращаетя среднее отношение числа свидетелей к числу вида
    вида n=p*q*r.

    Перед расчетом выполняется заполнение словаря _div_dict для оптимизации
    последующих опреаций.
    Прим.: до какого-то момента использование map_async замедляет программу.
    '''
    list_pqr = find_list_pqr_primes(n)

    primes_1 = (psnp.primes(2, n // (2 * 3)) - 1).tolist()
    if len(_div_dict) < len(primes_1):
        _init_div_dict(n, primes_1)
    primes_1.clear()

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
        raise Exception("Количество n=pqr равно 0!")


def calc_for_one_number_pairs():
    '''Функция-пример расчетывает среднее отношение для чисел вида n=p*q.
    '''
    mp.freeze_support()
    if _primes_frozenset is None:
        _init_primes_to_n_max()

    print('Введите число: n =', end=' ')
    n = int(input())
    if n > _n_max:
        raise Exception("Введеное число больше N_MAX={}!".format(_n_max))

    st = time.time()
    ratio = find_ratio_of_number_pairs(n)
    et = time.time()

    print('=' * 80)
    print("Среднее отношение:\t{}".format(ratio))
    print("Время расчета (c.):\t{:.3f}".format(et - st))
    print('=' * 80)


def find_ratios_for_n_list_pairs(n_list):
    '''Функция возвращает список из точечно посчитанных средних отношений
    для чисел вида n=p*q.
    '''
    st = time.time()
    ratios = [find_ratio_of_number_pairs(i) for i in n_list]
    et = time.time()
    print("Время расчета для n=pq (c.):  \t{:.3f}".format(et - st))

    return ratios


def find_ratios_for_n_list_pqr(n_list):
    '''Функция возвращает список из точечно посчитанных средних отношений
    для чисел вида n=p*q*r.
    '''
    st = time.time()
    ratios = [find_ratio_of_number_pqr(i) for i in n_list]
    et = time.time()
    print("Время расчета для n=pqr (c.):  \t{:.3f}".format(et - st))

    return ratios


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
        raise Exception("Ошибка ввода!")

    return n_list, filename_pdf


def main(*args):
    n_list, filename_pdf = args
    if n_list is None or filename_pdf is None:
        return

    mp.freeze_support()
    if _primes_frozenset is None:
        _init_primes_to_n_max()

    _init_div_dict(n_list[len(n_list) - 1])

    f = plt.figure()
    plt.style.use('ggplot')
    plt.title(
        "Cреднее отношение числа свидетелей к числу\n" +
        "для составных чисел $n$ меньших $N$"
    )
    plt.xlabel(r'$N$')
    plt.ylabel('Среднее отношение')
    plt.plot(n_list, find_ratios_for_n_list_pairs(n_list), label=r'$n=pq$')
    plt.plot(n_list, find_ratios_for_n_list_pqr(n_list), label=r'$n=pqr$')
    plt.legend()
    plt.show()
    f.savefig(filename_pdf, bbox_inches='tight')


if __name__ == '__main__':
    main(*init_n_list_and_filename_pdf())
