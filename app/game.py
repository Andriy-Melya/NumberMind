from random import shuffle

def set_number(n):
    N = [str(i) for i in range(10)]
    shuffle(N)
    while N[0] == '0':
        shuffle(N)
    return ''.join(N[:n])

def is_norm(x, N):
    try:
        n = int(x)
    except:
        return False
    if not(10 ** (N - 1) <= n <= 10 ** N):
        return False
    mas = []
    while n > 0:
        x = n % 10
        n //= 10
        if x in mas:
            return False
        else:
            mas.append(x)
    return True

def bulls_and_cows(x, y):
    B, K = 0, 0
    X = list(x)
    Y = list(y)
    for el in X:
        if el in Y:
            B += 1
    for i in range(len(X)):
        if X[i] == Y[i]:
            K += 1
    return B, K

