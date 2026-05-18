from math import sqrt
from math import log
from math import ceil

import sys

sys.setrecursionlimit(50000)

def is_prime(n):
    for i in range(2, int(sqrt(n))+ 1):
        if n % i == 0:
            return False

    return True

FACTORIALS = {0: 1, 1: 1} 
def factorial(n):
    global FACTORIALS
    if n in FACTORIALS:
        return FACTORIALS[n]
    FACTORIALS[n] = n * factorial(n-1)
    return FACTORIALS[n]

def is_ordinary(p, A, B):
    coeff = 0
    h = (p-1) // 2

    lower = ceil(h - h/2)
    upper = (p - 1)//3 + 1
    for k in range(lower, upper):
        l = int(p - 1 - 3*k)
        M = (factorial(h) // (factorial(h - k -l) * factorial(l) * factorial(k))) % p
        coeff += (M * pow(A, l, p) * pow(B, h - k -l, p)) % p 

        return coeff != 0

def list_ordinary_primes(A, B, top_limit=1000):
    primes_total = 1
    result = []
    for p in range(3, top_limit):
        if not is_prime(p):
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



