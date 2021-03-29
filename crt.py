"""
This file contains functions which are necessary to use Chinese Reminder Theorem
"""
from functools import reduce
from sage.all import *
from mapping import Mapping


def map2dict(F, imaginary, p=None):
    """
    This function converts polynomial mapping F (defined as list of n polynomials) into dictionary.
    The keys in this dictionary are tuples (i, a) where
    - i is the index of polynomial F_i in list F
    - a is a list of exponents in monomial
    The value for specified key is a list consisting of coefficient
    in F_i standing next to monomial defined by exponents.
    If the mapping F is defined over finite field the value is a list consisting
    of tuple of coefficient and prime number p
    :param F: Polynomial mapping defined over ring R
    :param imaginary: flag if input mapping is defined over field with imaginary part
    :param p: prime number
    :return: Dictionary { (i, a) => [coefficient] } or dictionary { (i, a) => [(coefficient, p)] }
    """
    if imaginary:
        zz = GaussianIntegers()
    else:
        zz = ZZ
    if p is None:
        return {(i, m.degrees()): [zz(c)] for i, f in enumerate(F) for m,c in zip(f.monomials(), f.coefficients())}
    else:
        return {(i, m.degrees()): [tuple((p, zz(c)))] for i, f in enumerate(F) for m,c in zip(f.monomials(), f.coefficients())}


def get_monomial(R, a):
    """
    Function is used to transform tuple of exponents to monomial
    :param R: ring
    :param a: tuple of exponents
    :return:
    """
    result = R("1")
    for x, p in zip(R.gens(), a):
        result *= x**p
    return result


def dict2map(D, mapping):
    """
    Function transforms the dictionary of form { (i, a) => coefficient } into polynomial mapping
    :param D: dictionary
    :param mapping: object defining mapping to inverse
    :return: polynomial mapping F = (F_1, ..., F_n)
    """
    F = [mapping.R("0") for _ in range(mapping.n)]
    for i, k in D:
        x = D[(i, k)]
        F[i] += mapping.R(str(x))*get_monomial(mapping.R, k)
    return Mapping([str(f) for f in F], name=mapping.name+"^{-1}",
                   field=mapping.R.base_ring(), imaginary=mapping.imaginary, r=1)


def is_there_prime(list_of_coefficients, prime):
    for p, c in list_of_coefficients:
        if p == prime:
            return True
    return False


def fill_gaps(C, primes):
    for t in C:
        list_of_coefficients = C[t]
        for prime in primes:
            if not is_there_prime(list_of_coefficients, prime):
                list_of_coefficients.append((prime, 0))
    return C


def dicts_union(A, B):
    """
    Function calculates some kind of sum of two dictionaries
    :param A: Dictionary in form { (i, a) => [(coefficient_A, p_A)] }
    :param B: Dictionary in form { (i, a) => [(coefficient_B, p_b)] }
    :return: Dictionary in form { (i, a) => [(coefficient_A, p_A), (coefficient_B, p_B)] }
    """
    result = {k: [] for k in A.keys() | B.keys()}
    for k in A:
        result[k] += A[k]
    for k in B:
        result[k] += B[k]
    return result


def sub_crt(n, m, N):
    """
    This function is used to calculate the value of Chinese Remainder Theorem for numbers n with modulis n
    :param n: numbers to solve system of congruences
    :param m: modulis of this system of congruences
    :param N: product of modulis
    :return: result of CRT with minimum absolute value (for more details see article)
    """
    temp = ZZ(IntegerModRing(N)(CRT(n, m)))
    t1 = N - temp
    if t1 < temp:
        temp = -t1
    return temp


def only_real(n):
    """
    Function checks if all numbers in input list n are real only
    :param n: list of numbers
    :return: True if all numbers are real
    """
    return all(imag(x) == 0 for x in n)


def only_imaginary(n):
    """
    Function checks if all numbers in input list n have only imaginary part
    :param n: list of numbers
    :return: True if no number has real part
    """
    return all((real(x) == 0 and imag(x) != 0) or (real(x) == 0 and imag(x) == 0) for x in n)


def crt(D, R):
    """
    Function uses Chinese Reminder Theorem to obtain the result.
    For every monomial we have list of tuples (c_i, p_i) which satisfy the following system of congruences:
    x = c_1 mod p_1
    x = c_2 mod p_2
    ...
    x = c_k mod p_k
    Chinese Reminder Theorem gives number c such that x = c mod (p_1p_2...p_k).
    It is our candidate for coefficient standing next to monomial a in polynomial F_i
    :param D: Dictionary in form { (i, a) => [(c_1, p_1), (c_2, p_2), ..., (c_k, p_k)] }
    :param R: polynomial ring of resulting mapping
    :return: Dictionary in form { (i, a) => c }
    """
    result = {}
    for k in D:
        m = [t[0] for t in D[k]]
        n = [t[1] for t in D[k]]
        N = reduce(lambda x, y: x*y, m)
        if only_real(n):
            n = [ZZ(t) for t in n]
            is_real = True
        elif only_imaginary(n):
            n = [ZZ(imag(t)) for t in n]
            is_real = False
        else:
            assert 1 == 2
        temp = sub_crt(n, m, N)
        if not is_real:
            temp = R(f'{temp}*I')
        result[k] = temp
    return result
