"""
This file contains functions used to clear denominators in the input mapping F
"""
import sys
from sage.all import *


def segre_homotopy(F, R, r):
    """
    Function implements Segre homotopy
    :param F: Polynomial mapping defined over ring R
    :param R: ring
    :param r: chosen element r
    :return: Function translated using Segre homotopy
    """
    n_X = [r*x for x in R.gens()]
    return [f(n_X)/r for f in F]


def reduce_mapping(F, p):
    """
    This function reduces polynomial mapping F modulo prime number p
    :param F: Polynomial mapping defined over ring R
    :param p: prime number
    :return: reduced modulo p polynomial mapping
    """
    var_names = ['X{0}'.format(i+1) for i in range(len(F))]
    if is_prime(p):
        Rp = PolynomialRing(GF(p), var_names)
    else:
        Rp = PolynomialRing(IntegerModRing(p), var_names)
    rFp = [Rp(str(f)) for f in F]
    return Rp, rFp

