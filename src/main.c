#include <flint/flint.h>
#include "ordinary.h"

int main(int argc, char** argv)
{
    flint_printf("%s\n", FLINT_VERSION);

    ulong p = 5;
    slong A = 1;
    slong B = 1;

    int result = is_ordinary(p, A, B);
    printf("%d\n", result);

    flint_cleanup_master();
}
