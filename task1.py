def add_of_GF(a, b, p):
    return (a + b) % p


def mul_of_GF(a, b, p):
    return (a * b) % p


def sub_of_GF(a, b, p):
    return add_of_GF(a, -b, p)


def xgcd(a, b):
    '''
    Iterative Extended Euclidean algorithm
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
    b_inv = mul_inv_of_GF(b, p)
    return mul_of_GF(a, b_inv, p)


def find_ord_val_GF(q, p):
    if p == 1 or p < q or p % q == 0:
        return -1

    t = q % p
    my_ord = 1

    while t != 1:
        t = mul_of_GF(t, q, p)
        my_ord += 1

    return my_ord


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
