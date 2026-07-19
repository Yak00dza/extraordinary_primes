from ordinary import list_ordinary_primes
from extraordinary import is_extraordinary
from datetime import datetime

def main(filename):
    DEPTH = 750
    START = 500
    result_file = 'curves_noniso_l_500-750_results.txt'
    with open(filename, 'r') as f:
        for curve in f:
            data = {'extraordinary': [], 'count': 0}
            A, B = map(lambda x: int(x.split('=')[1]), curve.strip().split(","))
            print(f"{datetime.now()}: Processing curve A={A}, B={B}")
            oprimes, _ = list_ordinary_primes(A, B, DEPTH, start=START)
            print(f"{datetime.now()}: Found {len(oprimes)} ordinary primes for curve A={A}, B={B}")
            extraordinary_primes = [p for p in oprimes if is_extraordinary(p, A, B)]
            print(f"{datetime.now()}: Found {len(extraordinary_primes)} extraordinary primes for curve A={A}, B={B}")
            data['extraordinary'].extend(extraordinary_primes)
            data['count'] += len(extraordinary_primes)

            with open(result_file, 'a') as rf:
                rf.write(f'{{"A": {A}, "B": {B}, "extraordinary": {data["extraordinary"]}, "count": {data["count"]}}}\n')

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python mass_analysis.py <filename>")
        sys.exit(1)
    main(sys.argv[1])