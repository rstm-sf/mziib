import sys
sys.path.append("../task1/")
from arithmetic_of_GF import *
import time


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


def list_sieve_of_Atkin(n):
    if 1 < n < 6:
        if n == 2:
            return [2]
        elif n == 5:
            return [2, 3, 5]
        else:
            return [2, 3]

    sqrt_n = int(math.sqrt(n))
    is_prime = [False for i in range(n + 1)]
    is_prime[2], is_prime[3] = True, True

    # Предположительно простые - это целые с нечетным числом
    # представлений в данных квадратных формах.
    # x2 и y2 - это квадраты i и j (оптимизация).
    x2 = 0
    for i in range(1, sqrt_n + 1):
        x2 += 2 * i - 1
        y2 = 0
        for j in range(1, sqrt_n + 1):
            y2 += 2 * j - 1
            k = 4 * x2 + y2
            if k <= n and (k % 12 == 1 or k % 12 == 5):
                is_prime[k] = not is_prime[k]
            # n = 3 * x2 + y2
            k -= x2
            if k <= n and k % 12 == 7:
                is_prime[k] = not is_prime[k]
            # k = 3 * x2 - y2
            k -= 2 * y2
            if i > j and k <= n and k % 12 == 11:
                is_prime[k] = not is_prime[k]

    # Отсеиваем квадраты простых чисел в интервале [5, sqrt(n)].
    # (основной этап не может их отсеять)
    for i in range(5, sqrt_n + 1):
        if is_prime[i]:
            k = i * i
            for j in range(k, n + 1, k):
                is_prime[j] = False

    primes = [2, 3, 5]
    primes.extend(
        i for i in range(6, n + 1)
        if is_prime[i] and i % 3 != 0 and i % 5 != 0
    )

    return primes


def find_list_pairs_primes(n):
    primes = list_sieve_of_Atkin(n // 2)
    len_primes, pairs = len(primes), list()

    while len_primes > 1:
        p, len_primes = primes.pop(), len_primes - 1
        for i in primes:
            if i * p <= n:
                pairs.append([i, p])
            else:
                break

    return pairs


def find_ratio_for_number(n):
    pairs = find_list_pairs_primes(n)
    len_pairs, i = len(pairs), 0
    ratios_n = np.empty(len_pairs)
    for pq in pairs:
        p, q = pq[0], pq[1]
        nw = find_number_witness_pq(p, q)
        ratios_n[i] = nw / (p * q)
        i += 1

    return np.sum(ratios_n) / len_pairs


def main():
    print('Введите число: n =', end=' ')
    n = int(input())

    start_time = time.time()
    ratio = find_ratio_for_number(n)
    end_time = time.time()

    print('=' * 80)
    print("Среднее соотношение:\t{}".format(ratio))
    print("Время расчета (c):  \t{:.6f}".format(end_time - start_time))
    print('=' * 80)


if __name__ == '__main__':
    main()
