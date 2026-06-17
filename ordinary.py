from math import sqrt
from math import log
from math import ceil
from flint import *
import sys

sys.setrecursionlimit(50000)

def is_prime(n):
    for i in range(2, int(sqrt(n))+ 1):
        if n % i == 0:
            return False

    return True

def is_ordinary(p, A, B):
    F = fmpz_mod_ctx(p)

    A = F(A)
    B = F(B)

    h = (p - 1) // 2

    lower = ceil(h - h / 2)
    upper = (p - 1) // 3 + 1

    coeff = F(0)

    for k in range(lower, upper):
        l = p - 1 - 3 * k
        if l < 0:
            continue

        num = fmpz.fac_ui(h)
        den = fmpz.fac_ui(h - k - l) * fmpz.fac_ui(l) * fmpz.fac_ui(k)

        M = (num // den) % p
        M = F(M)

        coeff += M * (A ** l) * (B ** (h - k - l))

    return coeff != 0


def list_ordinary_primes(A, B, top_limit=1000):
    result = []
    primes_total = 0

    for p in range(3, top_limit):
        if not fmpz(p).is_prime():
            continue

        primes_total += 1

        if is_ordinary(p, A, B):
            result.append(p)

    return result, primes_total

def has_complex_multiplication(A, B, oprimes, primes_total):
    density = len(oprimes) / primes_total
    return density < 0.55



def main():
    A = int(input('A: ')) 
    B = int(input('B: '))
    top_limit = int(input('Upper bound: '))

    oprimes, primes_total = list_ordinary_primes(A, B, top_limit)
    print(f'Found {len(oprimes)} ordinary primes out of {primes_total} primes less than {top_limit}.')
    if has_complex_multiplication(A, B, oprimes, top_limit):
        print('Based on the ensity, the curve is expected to have complex multiplication')
    else:
        print('Based on the ensity, the curve is expected to NOT have complex multiplication')
    

if __name__ == '__main__':
    main()



