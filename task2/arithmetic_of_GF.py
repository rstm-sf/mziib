import math
import numpy as np
import random


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


n_for_Atkin = int(1e7)
print("Генерация решета Аткина до N={}...".format(n_for_Atkin))
primes_tuple = tuple(list_sieve_of_Atkin(n_for_Atkin))
primes_frozenset = frozenset(primes_tuple)
print("Решето Аткина сгенерировано.")


def is_even(n):
    return n % 2 == 0


def add_of_GF(a, b, p):
    return (a + b) % p


def mul_of_GF(a, b, p):
    return (a * b) % p


def sub_of_GF(a, b, p):
    return (a - b) % p


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def xgcd(a, b):
    '''Iterative Extended Euclidean algorithm
    '''
    x0, x1, y0, y1 = 1, 0, 0, 1

    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return a, x0, y0


def mul_inv_of_GF(a, p):
    g, x, _ = xgcd(a, p)
    if g == 1:
        return x % p


def div_of_GF(a, b, p):
    if b == 0:
        return "Bad value of 'b'"

    b_inv = mul_inv_of_GF(b, p)
    return mul_of_GF(a, b_inv, p)


def find_ord_val_GF(q, p):
    if p < 2 or p % q == 0:
        return "Bad value of 'p'"

    t = q % p
    my_ord = 1

    while t != 1:
        t = mul_of_GF(t, q, p)
        my_ord += 1

    return my_ord


def is_prime_number(n):
    '''Checks the number on prime

    Use the trial division.
    '''
    for i in range(2, math.ceil(math.sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True


def function_Euler(n):
    '''Euler’ totient function
    '''
    if n == 1:
        return 1
    if n in primes_frozenset:
        return n - 1

    value, i = n, 2
    while i * i <= n:
        if n % i == 0:
            i_inv = 1. / i
            n *= i_inv
            while n % i == 0:
                n *= i_inv
            value *= 1 - i_inv
        i += 1
    if n > 1:
        value *= 1 - 1. / n

    return int(value)


def find_bin_and_remainder_for_number(n):
    s, t = 0, n
    while is_even(t):
        s += 1
        t = t // 2
    return s, t


def find_s_and_t_for_witness(n):
    '''Find s and t for n - 1 = t*2**s
    '''
    s, t = find_bin_and_remainder_for_number(n - 1)
    return s, t


def is_witness_prime_number(a, n, s=None, t=None):
    if is_even(n):
        return "'n' not odd"

    if t is None:
        s, t = find_s_and_t_for_witness(n)

    n_1 = n - 1

    b = math.pow(a, t) % n
    if b == 1 or b == n_1:
        return True

    i, b2 = 1, mul_of_GF(b, b, n)
    b = b2
    while i < s:
        if b == 1:
            return False
        elif b == n_1:
            return True
        i += 1
        b = mul_of_GF(b, b2, n)

    return False


def generate_set_randint(low, high=None, size=None):
    if size is not None and high - low <= size:
        return "Bad input values"

    if size == 1 or size is None:
        if high is None:
            high = low
            low = 0
        gen_set = {random.randint(low, high)}
    else:
        gen_set = set(np.random.randint(low, high, size))
        while len(gen_set) < size:
            gen_set.add(random.randint(low, high))

    return gen_set


def test_Miller_Rabin(k, n):
    if n < 2 or is_even(n):
        return False

    a = generate_set_randint(2, n, k)
    for i in a:
        if gcd(i, n) != 1:
            return False

    s, t = find_s_and_t_for_witness(n)
    for i in a:
        if not is_witness_prime_number(i, n, s, t):
            return False

    return True


def task_find_ord():
    print('Введите числа: q - любое число конечного поля F(p), p - порядок поля.')

    print('p = ', end='')
    p = int(input())
    if p < 2:
        print('Неверное число!')

    print('q = ', end='')
    q = int(input())
    if q < 0:
        print('Неверное число!')

    print('Порядок числа q конечного поля F(p) равен:', end=' ')
    print(find_ord_val_GF(q, p))
