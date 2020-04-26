"""
This file contains functions which are necessary to use Chinese Reminder Theorem
"""
import sys
from sage.all import *
from functools import reduce


def map2dict(F, p=None):
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
    :param p: prime number
    :return: Dictionary { (i, a) => [coefficient] } or dictionary { (i, a) => [(coefficient, p)] }
    """
    D = {}
    for i, f in enumerate(F):
        for k in f.dict():
            if p is None:
                D[(i,k)] = [int(f.dict()[k])]
            else:
                v1 = int(f.dict()[k])
                v2 = -(p-v1)
                if abs(v1) <= abs(v2):
                    D[(i,k)] = [(p, v1)]
                else:
                    D[(i,k)] = [(p, v2)]
    return D


def get_monomial(R, a):
    """
    Function is used to transform tuple of exponents to monomial
    :param R: ring
    :param a: tuple of exponents
    :return:
    """
    result = R("1")
    for x,p in zip(R.gens(), a):
        result *= x**p
    return result


def dict2map(D, R):
    """
    Function transforms the dictionary of form { (i, a) => coefficient } into polynomial mapping
    :param D: dictionary
    :param R: ring
    :return: polynomial mapping F = (F_1, ..., F_n)
    """
    F = [R("0") for x in R.gens()]
    for i,k in D:
        F[i] += R(str(D[(i,k)]))*get_monomial(R,k)
    return F


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


def crt(D):
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
    :return: Dictionary in form { (i, a) => c }
    """
    result = {}
    for k in D:
        m = [t[0] for t in D[k]]
        n = [t[1] for t in D[k]]
        N = reduce(lambda x, y: x*y, m)
        temp = CRT(n,m)
        t1 = N - temp
        if abs(t1) < abs(temp):
            temp = -t1
        result[k] = temp
    return result
