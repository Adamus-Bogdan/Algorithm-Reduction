"""
This file contains at implementation of ABCH algorithm.
Description of this algorithm can be found in article:
"An effective study of polynomial maps"
See details in README.md file.
"""
import sys
from tqdm import tqdm
from functools import reduce
from sage.all import *
from mapping import Mapping


def get_terms(p):
    """
    This function gets the n-variable polynomial p and returns list of terms in this polynomial
    :param p: n-variable polynomial
    :return: list of terms which sum to polynomial p
    """
    return [m*c for m,c in zip(p.monomials(), p.coefficients())]


def filter_terms(p, R, degree_limit):
    """
    This function gets the n-variable polynomial p and the number degree_limit
    and returns the polynomial which consists of terms of degree at most degree_limit
    :param p: n-variable polynomial
    :param R: polynomial ring of n-variable polynomial p
    :param degree_limit: boundary for degree
    :return: n-variable polynomial with terms of degree at most limit
    """
    for m, c in [(m,c) for m,c in zip(p.monomials(), p.coefficients()) if m.degree() > degree_limit]:
        p -= m*c
    return p


def find_degrees(mapping):
    """
    This function calculates value D, d and list [d_1,...,d_n] (for details see README.md file)
    :param mapping: object defining mapping to inverse
    :return: tuple: (D, d, [d_1, ..., d_n])
    """
    # we put max int value as d parameter
    min_d = sys.maxsize
    max_D = -1
    lower_degrees = []
    for f, x in zip(mapping.F, mapping.R.gens()):
        monomials = (f - x).monomials()
        if len(monomials) == 0:
            lower_degrees.append(sys.maxsize)
        else:
            temp_degrees = [m.degree() for m in monomials]
            d = min(temp_degrees)
            if d < min_d:
                min_d = d
            D = max(temp_degrees)
            if D > max_D:
                max_D = D
            lower_degrees.append(d)
    return max_D, min_d, lower_degrees


def seq_substitute(p, mapping, degree_limit, debug):
    """
    This function calculates value of polynomial p for arguments defined in list F.
    This function gets only these terms which degree is at most degree_limit.
    It uses sequential computation.
    :param p: polynomial to calculate value of
    :param mapping: object defining mapping to inverse
    :param degree_limit: maximum degree of resulting polynomial
    :param debug: flag if function should print additional output
    :return:
    """
    result = 0
    terms = get_terms(p)
    if debug:
        terms = tqdm(terms)
    for term in terms:
        temp = term(mapping.F)
        result += filter_terms(temp, mapping.R, degree_limit)
    return result


def parallel_substitute(p, mapping, degree_limit, debug):
    """
    This function calculates value of polynomial p for arguments defined in list F.
    This function gets only these terms which degree is at most degree_limit.
    It uses parallel computation.
    :param p: polynomial to calculate value of
    :param mapping: object defining mapping to inverse
    :param degree_limit: maximum degree of resulting polynomial
    :param debug: flag if function should print additional output
    :return:
    """
    terms = get_terms(p)
    if len(terms) < 20:
        return seq_substitute(p, mapping, degree_limit, debug)
    S = RecursivelyEnumeratedSet(terms, lambda x: [], structure='forest', category=FiniteEnumeratedSets()) 
    return S.map_reduce(lambda t: seq_substitute(t, mapping, degree_limit, debug), lambda a, b: a+b, mapping.R("0"))


def inverse_algorithm(mapping, x, substitute, debug):
    """
    This function obtain an inverse of i-th coordinate of input polynomial mapping F
    :param mapping: object defining mapping to inverse
    :param x: coordinate to inverse
    :param substitute: function used to perform substitution (sequential vs parallel)
    :param debug: flag if debug should be printed to standard output
    :return: G_i - i-th coordinate of global inverse mapping G
    """
    if debug:
        print('---------------------------------------------')
        print(f'Executing algorithm for {x}')
    p = x
    result = x
    step = 1
    max_D, min_d, lower_degrees = find_degrees(mapping)
    degree_limit = max_D**(mapping.n-1)
    i = mapping.R.gens().index(x)
    if min_d > 1:
        limit = floor((max_D**(mapping.n - 1) - lower_degrees[i])/(min_d - 1) + 1)+1
    else:
        limit = degree_limit
    if lower_degrees[i] == sys.maxsize:
        if debug:
            print('There is no need to perform the algorithm')
        return x
    if debug:
        print(f'Maximum number of steps: {limit}')
        print(f'Inversion degree boundary: {degree_limit}')
    while True:
        p -= substitute(p, mapping, degree_limit, debug)
        result += p

        if p == 0:
            if debug:
                print(f'P_{step} = 0')
            return result
        else:
            degrees = [m.degree() for m in p.monomials()]
            if debug:
                print(f'P_{step} has degree: {max(degrees)}, ldegree: {min(degrees)}, length: {len(degrees)}')
            if step == limit:
                if debug:
                    print('NOT PASCAL FINITE!')
                return result
        step += 1
    
    
def algorithm(mapping, debug, parallel=False):
    """
    This function obtain an inverse of input polynomial mapping F
    param F: Polynomial mapping defined over ring R
    :param mapping: object defining mapping to inverse
    :param debug: flag if debug should be printed to standard output
    :param parallel: flag if algorithm should be run in parallel
    :return: polynomial mapping G = F^{-1}
    """
    if debug:
        print(str(mapping))
    if parallel:
        subs = parallel_substitute
    else:
        subs = seq_substitute
    g = [inverse_algorithm(mapping, x, subs, debug) for x in mapping.R.gens()]
    r = Mapping(["0"]*len(g))
    r.F = g
    r.n = len(g)
    r.R = g[0].parent()
    r.name = mapping.name+"^{-1}"
    r.primes = []
    r.r = 1
    r.imaginary = mapping.imaginary
    return r
