import random
from math import ceil
from decimal import Decimal

MAX_RANGE = 10 ** 3


def reconstruct_secret(shares):
    # shares in the form (x, y)
    # coefficients = []
    res = 0
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        delta_i = Decimal(1)
        for i, share_i in enumerate(shares):
            xi, _ = share_i  # we don't need yi
            if i != j:
                # not considering the same share while computing prod
                delta_i *= Decimal(xi) / Decimal(xi - xj)
        # multiply by the y value of current share
        delta_i *= yj
        res += Decimal(delta_i)
        # coefficients.append(delta_i)
    # print_polynomial(coefficients)
    return int(round(Decimal(res), 0))


def evaluate_polynomial(coefficients, x):
    result = 0
    for i in range(len(coefficients)):
        result += coefficients[i] * (x ** i)
    return result


def generate_coefficients(t, secret):
    coefficients = [secret]
    for i in range(1, t):
        coefficients.append(random.randint(0, MAX_RANGE))
    return coefficients


def print_polynomial(coefficients):
    print("f(x) = ", end="")
    for i in range(len(coefficients)):
        print(coefficients[i], end="")
        if i != 0:
            if i != len(coefficients) - 1:
                print(f"(x^{i}) + ", end="")
                # print("x^", i, " + ", end="")
            else:
                print(f"(x^{i})", end="")
        else:
            print(f" + ", end="")

    print()


def generate_shares(secret, n, t):
    # shares in the form (x, y)
    coefficients = generate_coefficients(t, secret)
    print_polynomial(coefficients)
    shares = []
    for i in range(1, n + 1):
        x = random.randint(1, MAX_RANGE)
        shares.append((x, evaluate_polynomial(coefficients, x)))
    return shares


if __name__ == "__main__":

    # secret = random.randint(0, MAX_RANGE)
    # print(f"Secret: {secret}\n")
    secret = int(input("Enter secret: "))
    n = int(input("Enter n: "))
    t = int(input("Enter t: "))
    if t > n:
        raise ValueError("t must be less than or equal to n")
    shares = generate_shares(secret, n, t)
    # shares = [(5, 3), (7, 2), (12, 6), (30, 15)]
    print(f"Shares: {shares}\n")
    # pool = random.sample(shares, t)
    input_t = int(input("Enter number of shares for decryption: "))
    pool = []
    for i in range(input_t):
        tup = tuple(map(int, input(f"Enter x and y comma separated for share #{i+1}: ").split(",")))
        pool.append(tup)
    # for i in range(t):
    #     t = input()
    #     a = tuple(int(x) for x in t.split())
    #     #view this tuple
    #     print(a)
    print(f"Reconstructed secret: {reconstruct_secret(pool)}")
