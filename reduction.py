import sys
from sage.all import *

def segre_homotopy(F, R, r):
    n_X = [r*x for x in R.gens()]
    return [f(n_X)/r for f in F]

def reduce_mapping(F, p):
    var_names = ['X{0}'.format(i+1) for i in range(len(F))]
    if is_prime(p):
        Rp = PolynomialRing(GF(p), var_names)
    else:
        Rp = PolynomialRing(IntegerModRing(p), var_names)
    rFp = [Rp(str(f)) for f in F]
    return Rp, rFp

