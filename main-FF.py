"""
This file contains program which inverts the mapping using our improved approach
"""
import sys
from time import time
from algorithm import algorithm
from crt import map2dict, dict2map, dicts_union, crt
from reduction import reduce_mapping, segre_homotopy
from utils import check_inversion
from simple_mapping import F, R

if __name__ == '__main__':
    BEGIN = time()
    # Step 1: clear denominators in input mapping F
    F = segre_homotopy(F, R, 3)
    # Step 2: specify prime numbers to reduce mapping F
    primes = [3,5,7,11,13,17,19,23]
    
    C = {}
    # Step 3: for every prime number p
    for p in primes:
        # Step 3.1: reduce mapping F modulo p
        Rp, Fp = reduce_mapping(F,p)
        begin = time()
        # Step 3.2: perform base algorithm for reduced maping
        Gp = algorithm(Fp, Rp, False)
        end = time()
        print("Time necessary to inverse {0}-reduced mapping: {1}".format(p, end - begin))
        # Step 3.3: transform inversion of reduced mapping into dictionary
        Dp = map2dict(Gp, p)
        # Step 3.4: remember the coefficients in this mapping
        C = dicts_union(C, Dp)

    # Step 4: Use Chinese Reminder Theory to obtain candidate for global inverse
    D = crt(C)
    G = dict2map(D, R)
    END = time()
    # Step 5: Check if candidate is really inverse
    check_inversion(F, G, R)
    print("Time necessary to inverse mapping: {0}".format(END - BEGIN))


