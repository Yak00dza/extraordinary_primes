from math import sqrt
from math import log
from math import ceil
from flint import *
import sys
import os

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

    if A == 0 or B == 0:
        return False

    h = (p - 1) // 2

    lower = (h + 1) // 2          # ceil(h/2)
    upper = (p - 1) // 3 + 1

    if lower >= upper:
        return False

    k = lower
    l = 2*h - 3*k
    m = 2*k - h

    num = fmpz.fac_ui(h)
    den = (
        fmpz.fac_ui(k)
        * fmpz.fac_ui(l)
        * fmpz.fac_ui(m)
    )

    T = F((num // den) % p)
    T *= A**l
    T *= B**m

    coeff = T

    A3inv = (A**3).inverse()
    B2 = B*B

    for k in range(lower, upper - 1):
        l = 2*h - 3*k
        m = 2*k - h

        T *= F(l*(l-1)*(l-2))
        T *= B2

        T *= F((k+1)*(m+1)*(m+2)).inverse()
        T *= A3inv

        coeff += T

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
    DEPTH = int(1e7)

    curves = []
    with open('curves.txt', 'r') as f:
        for line in f:
            s1, s2 = line.split(',')
            A, B = map(lambda x: int(x.split('=')[1]), (s1, s2))
            curves.append((A, B))

    out_dir = 'ordinary_primes'
    os.makedirs(out_dir, exist_ok=True)

    p = fmpz(3)
    while p < DEPTH:
        if not is_prime(p):
            p += 1
            continue

        for A, B in curves:
            if is_ordinary(p, A, B):
                filename = f'{out_dir}/A={A}_B={B}.txt'
                with open(filename, 'a') as f:
                    f.write(f'{p}\n')
        
        p += 1


    

if __name__ == '__main__':
    main()



