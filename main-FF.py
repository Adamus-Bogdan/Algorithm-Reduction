import sys
from time import time
from algorithm import algorithm
from crt import map2dict, dict2map, dicts_union, crt
from reduction import reduce_mapping, segre_homotopy
from utils import check_inversion
from simple_mapping import F, R

if __name__ == '__main__':
    BEGIN = time()
    
    F = segre_homotopy(F, R, 3)
    primes = [3,5,7,11,13,17,19,23]
    
    C = {}
    for p in primes:
        Rp, Fp = reduce_mapping(F,p)
        begin = time()
        Gp = algorithm(Fp, Rp, False)
        end = time()
        print("Time necessary to inverse {0}-reduced mapping: {1}".format(p, end - begin))
        check_inversion(Fp, Gp, Rp)
        Dp = map2dict(Gp, p)
        C = dicts_union(C, Dp)

    D = crt(C)
    G = dict2map(D, R)
    END = time()
    check_inversion(F, G, R)
    print("Time necessary to inverse mapping: {0}".format(END - BEGIN))


