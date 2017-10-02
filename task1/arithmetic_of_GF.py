import math
import numpy as np
import random


def add_of_GF(a, b, p):
    return (a + b) % p


def mul_of_GF(a, b, p):
    return (a * b) % p


def sub_of_GF(a, b, p):
    return (a - b) % p


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
    for i in range(2, math.ceil(math.sqrt(n)), 1):
        if n % i == 0:
            return False

    return True


def function_Euler(n):
    '''Euler’ totient function
    '''
    value = 0
    for i in range(1, n, 1):
        d, _, _ = xgcd(n, i)
        if d == 1:
            value += 1

    return value


def find_s_and_t_for_witness(n):
    '''Find s and t for n - 1 = t*2**s
    '''
    if n % 2 == 0:
        return "'n' not odd"

    s, t = 1, (n - 1) >> 1
    while t % 2 == 0:
        s += 1
        t = t >> 1

    return s, t


def is_witness_prime_number(a, n, s=None, t=None):
    if n % 2 == 0:
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


def generate_set_randint(low=0, high=None, size=None):
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
    a = generate_set_randint(2, n, k)
    for i in a:
        if n % i == 0:
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
