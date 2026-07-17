from math import ceil
from flint import *
from flint import fmpz_mod_mat as matrix

from datetime import datetime

Z = fmpz

def compute_d(p, A, B):
    r = (p - 1) // 2
    n = r + 1
    def d_raw(i):
        lower = max(0, (i - n + 1) // 2)   # ceil((i-n)/2)
        upper = min(n + 1, i // 3 + 1)

        if lower >= upper:
            return Z(0)

        k = lower
        l = i - 3*k
        m = n - k - l

        T = Z.fac_ui(n)
        T //= Z.fac_ui(k)
        T //= Z.fac_ui(l)
        T //= Z.fac_ui(m)
        T *= A**l
        T *= B**m

        total = T

        B2 = B * B
        A3 = A * A * A

        for k in range(lower, upper - 1):
            l = i - 3*k
            m = n - k - l

            T *= l * (l - 1) * (l - 2)
            T *= B2

            T //= (k + 1) * (m + 1) * (m + 2)
            T //= A3

            total += T

        return total

    d_values = [d_raw(i) for i in range(0, 3*r + 3 + 1)]

    def d(i):
        if i < 0 or i > 3*n:
            return Z(0)
        return d_values[i]

    return d

def compute_g(p, A, B):
    def g_raw(i):
        lower = max(0, (i - p + 1)//2)     # ceil((i-p)/2)
        upper = min(p + 1, i//3 + 1)

        if lower >= upper:
            return Z(0)

        k = lower
        l = i - 3*k
        m = p - k - l

        p_fac = Z.fac_ui(p)

        T = p_fac
        T //= Z.fac_ui(k)
        T //= Z.fac_ui(l)
        T //= Z.fac_ui(m)
        T *= A**l
        T *= B**m

        total = T

        B2 = B*B
        A3 = A*A*A

        for k in range(lower, upper - 1):
            l = i - 3*k
            m = p - k - l

            T *= l*(l-1)*(l-2)
            T *= B2

            T //= (k+1)*(m+1)*(m+2)
            T //= A3

            total += T

        return total

    r = int((p - 1) // 2)

    g_values = [g_raw(i) // p for i in range(0, 6*r + 1 + 1)]

    def g(i):
        if i < 0 or i > 6*r + 1:
            return 0

        if i == 3*p:
            return 0
        if i == p:
            return g_raw(i) - (A ** p)
        if i == 0:
            return 0

        return g_values[i]

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

    p2 = 2*p

    for i in range(0, m):
        if i == p:
            equations_augmented[i, m-1] -= A1
        if i == 0:
            equations_augmented[i, m-1] -= B1
        equations_augmented[i, m-1] += g(i)

        if i < k:
            equations_augmented[i, i] += A0
            equations[i, i] += A0

        h = i - p2
        if h >= 0 and h <= k:
            equations[i, h] += 3
            equations_augmented[i, h] += 3


        for j in range(0, 4*r + 1):
            equations[i, j+k] -= 2*d(i - j)
            equations_augmented[i, j+k] -= 2*d(i - j)

    rank = equations.rank()
    new_rank = equations_augmented.rank()


    if rank == new_rank:
        return True

    return False

if __name__ == '__main__':
    # get filename as an argument
    import sys
    if len(sys.argv) < 2:
        print('Usage: python extraordinary.py <filename>')
        sys.exit(1)
    path = sys.argv[1]
    filename = path.split('/')[-1]
    A, B = map(lambda x: int(x.split('=')[1]), filename.split('.')[0].split('_'))
    
    with open(path, 'r') as f:
        for line in f:
            p = int(line.strip())
            if is_extraordinary(p, A, B):
                print(f'Found extraordinary prime for A={A}, B={B}: {p}')
                with open(f'extraordinary_primes/{filename}', 'a') as out:
                    out.write(f'{p}\n')


    print('Finished at time:', datetime.now())


