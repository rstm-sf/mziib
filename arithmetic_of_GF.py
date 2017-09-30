import math


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


def is_witness_prime_number(a, n):
    if n % 2 == 0:
        return "'n' not odd"

    n_1 = n - 1
    s, t = 1, n_1 >> 1
    while t % 2 == 0:
        s += 1
        t = t >> 1

    b = math.pow(a, t) % n
    if b == 1 or b == n_1:
        return True

    i = 1
    while i < s:
        b = mul_of_GF(b, b, n)
        if b == 1:
            return False
        elif b == n_1:
            return True
        i += 1

    return False


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
