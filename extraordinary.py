from math import ceil
from flint import *
from flint import fmpz_mod_mat as matrix

from ordinary import list_ordinary_primes

Z = fmpz

def compute_d(p, A, B):
    def d(i):
        r = (p - 1) // 2
        if i < 0 or i > 3*r + 3:
            return 0

        lower = max(0, ceil(int((i - r - 1)) / 2))
        upper = min(int(r + 1 + 1), int(i // 3 + 1))

        r_fac = Z.fac_ui(r+1)
        def term(k):
            l = i - 3*k
            prod = Z(1)
            prod *= (r_fac) // (Z.fac_ui(k) * Z.fac_ui(l) * Z.fac_ui(r + 1 - k - l))
            prod *= A ** l
            prod *= B ** (r + 1 - k -l)
            return prod

        return sum([term(k) for k in range(lower, upper)])

    return d

def compute_g(p, A, B):
    def g_raw(i):
        lower = max(0, ceil(int(i - p) / 2))
        upper = min(int(p + 1), int(i // 3 + 1))
        p_fac = Z.fac_ui(p)
        def term(k):
            l = i - 3*k
            prod = Z(1)
            prod *= (p_fac) // (Z.fac_ui(k) * Z.fac_ui(l) * Z.fac_ui(p - k - l))
            prod *= A ** l
            prod *= B ** (p - k -l)
            return prod

        return sum([term(k) for k in range(lower, upper)])

    r = int((p - 1) // 2)

    def g(i):
        if i < 0 or i > 6*r + 1:
            return 0

        if i == 3*p:
            return 0
        if i == p:
            return g_raw(i) - (A ** p)
        if i == 0:
            return 0

        return g_raw(i) // p 

    return g

def extract_A1(A, p):
    F = fmpz_mod_ctx(p)
    F2 = fmpz_mod_ctx(p**2)
    A = F2(A)

    A1 = (A - A**p) / F2(p) 
    return F(int(A1))


# A and B are from Z mod p^2
def is_extraordinary(p, A, B):
    Z = fmpz
    p = Z(p)

    r = int((p - 1) // 2)

    A0 = A % p
    B0 = B % p

    A1 = extract_A1(A, p)
    B1 = extract_A1(B, p)

    d = compute_d(p, A, B)
    g = compute_g(p, A, B) 


    F = fmpz_mod_ctx(p)
    A0 = F(A0)
    B0 = F(B0)


    m = int(7*r + 4)
    k = 3*r + 2
    equations = matrix(m, m-1, F)
    equations_augmented = matrix(m, m, F)

    for i in range(0, m):
        if i == p:
            equations_augmented[i, m-1] -= A1
        if i == 0:
            equations_augmented[i, m-1] -= B1
        equations_augmented[i, m-1] += g(i)

        for j in range(0, 3*r + 1 + 1):
            if i == j:
                equations[i, j] += A0
                equations_augmented[i, j] += A0
            if j == i - 2*p:
                equations[i, j] += 3 
                equations_augmented[i, j] += 3 

        for j in range(0, 4*r + 1):
            equations[i, j+k] -= 2*d(i - j)
            equations_augmented[i, j+k] -= 2*d(i - j)


    rank = equations.rank()
    new_rank = equations_augmented.rank()

    if rank == new_rank:
        return True

    return False

if __name__ == '__main__':
    A, B = 1, 0
    oprimes, _ = list_ordinary_primes(A, B, top_limit=500)
    print('Finished listing ordinary primes')
    i = 1
    for oprime in oprimes:
        if i % 10 == 0:
            print(f'Checked {i} primes') 
        if is_extraordinary(oprime, A, B):
            print(oprime, end=' ')

        i += 1
    print()


