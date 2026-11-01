#include "ordinary.h"

int is_ordinary(ulong p, slong A_si, slong B_si)
{
    fmpz_mod_ctx_t mod_p;
    fmpz_mod_ctx_init_ui(mod_p, p);

    fmpz_t A;
    fmpz_t B;
    fmpz_mod_set_si(A, A_si, mod_p);
    fmpz_mod_set_si(B, B_si, mod_p);

    ulong h = (p-1)/2;

    ulong lower = floor(h / 3);
    ulong higher = floor(h / 2);

    fmpz_t sum;
    fmpz_zero(sum);

    fmpz_t term;
    fmpz_t binom1;
    fmpz_t binom2;
    fmpz_t A_pow;
    fmpz_t B_pow;
    for (ulong i = lower; i <= higher; ++i)
    {
        fmpz_one(term);
        ulong r = 3 * i - h;

        // Compute binomials
        fmpz_bin_uiui(binom1, h, i);
        fmpz_bin_uiui(binom2, i, r);

        // Raise to powers
        fmpz_mod_pow_ui(A_pow, A, r, mod_p);
        fmpz_mod_pow_ui(B_pow, B, r - 2 * i, mod_p);

        // Multiply everything
        fmpz_mod_mul_fmpz(term, binom1, binom2, mod_p);
        fmpz_mod_mul_fmpz(term, term, A_pow, mod_p);
        fmpz_mod_mul_fmpz(term, term, B_pow, mod_p);
        

        fmpz_mod_add(sum, sum, term, mod_p);
    }

    int result = !fmpz_is_zero(sum);


    fmpz_clear(binom1);
    fmpz_clear(binom2);
    fmpz_clear(sum);
    fmpz_clear(A);
    fmpz_clear(B);

    fmpz_mod_ctx_clear(mod_p);
    
    return result;
}
/*
    F = fmpz_mod_ctx(p)

    A = F(A)
    B = F(B)



    h = (p - 1) // 2

    ----> We are here

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
*/