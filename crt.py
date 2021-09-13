"""
This file contains functions which are necessary to use Chinese Reminder Theorem
"""
from sage.all import *
from mapping import Mapping


def map2dict(mapping, is_imaginary, p=None):
    """
    This function converts polynomial mapping F (defined as list of n polynomials) into dictionary.
    The keys in this dictionary are tuples (i, a) where
    - i is the index of polynomial F_i in list F
    - a is a list of exponents in monomial
    The value for specified key is a list consisting of coefficient
    in F_i standing next to monomial defined by exponents.
    If the mapping F is defined over finite field the value is a list consisting
    of tuple of coefficient and prime number p
    :param mapping: Polynomial mapping defined over ring R
    :param is_imaginary: flag if input mapping is defined over field with imaginary part
    :param p: prime number
    :return: Dictionary { (i, a) => [coefficient] } or dictionary { (i, a) => [(coefficient, p)] }
    """
    if is_imaginary:
        zz = GaussianIntegers()
    else:
        zz = ZZ
    if p is None:
        return {(index, m): [zz(c)] for index, f in enumerate(mapping) for m, c in f.dict().items()}
    else:
        return {(index, m): [(p, zz(c))] for index, f in enumerate(mapping) for m, c in f.dict().items()}


def dict2map(input_dictionary, mapping):
    """
    Function transforms the dictionary of form { (i, a) => coefficient } into polynomial mapping
    :param input_dictionary: dictionary
    :param mapping: object defining mapping to inverse
    :return: polynomial mapping F = (F_1, ..., F_n)
    """
    f = [mapping.R("0") for _ in range(mapping.n)]
    for index, k in input_dictionary:
        x = input_dictionary[(index, k)]
        f[index] += mapping.R({k: x})
    return Mapping(f, mapping.name+"^{-1}", mapping.R, [], 1, mapping.imaginary)


def is_there_prime(list_of_coefficients, prime):
    for p, c in list_of_coefficients:
        if p == prime:
            return True
    return False


def fill_gaps(coefficients, list_of_primes):
    for t in coefficients:
        list_of_coefficients = coefficients[t]
        for prime in list_of_primes:
            if not is_there_prime(list_of_coefficients, prime):
                list_of_coefficients.append((prime, 0))
    return coefficients


def dicts_union(a, b):
    """
    Function calculates some kind of sum of two dictionaries
    :param a: Dictionary in form { (i, a) => [(coefficient_A, p_A)] }
    :param b: Dictionary in form { (i, a) => [(coefficient_B, p_b)] }
    :return: Dictionary in form { (i, a) => [(coefficient_A, p_A), (coefficient_B, p_B)] }
    """
    result = {k: [] for k in a.keys() | b.keys()}
    for k in a:
        result[k] += a[k]
    for k in b:
        result[k] += b[k]
    return result


def my_crt(input_dictionary):
    """
    Function uses Chinese Reminder Theorem to obtain the result.
    For every monomial we have list of tuples (c_i, p_i) which satisfy the following system of congruences:
    x = c_1 mod p_1
    x = c_2 mod p_2
    ...
    x = c_k mod p_k
    Chinese Reminder Theorem gives number c such that x = c mod (p_1p_2...p_k).
    It is our candidate for coefficient standing next to monomial a in polynomial F_i
    :param input_dictionary: Dictionary in form { (i, a) => [(c_1, p_1), (c_2, p_2), ..., (c_k, p_k)] }
    :return: Dictionary in form { (i, a) => c }
    """
    result = {}

    for k, p in input_dictionary.items():
        mods = [t[0] for t in p]
        rems = [t[1] for t in p]
        prod_of_mods = reduce(lambda x, y: x*y, mods)

        temp1 = partial_crt(mods, prod_of_mods, rems, imag)
        temp2 = partial_crt(mods, prod_of_mods, rems, real)

        if temp1 == 0:
            temp = ZZ(temp2)
        else:
            temp = GaussianIntegers()(temp1*I + temp2)
        result[k] = temp
    return result


def partial_crt(mods, prod_of_mods, rems, chooser):
    inside_rems = [chooser(ir) for ir in rems]
    if all(ir == 0 for ir in inside_rems):
        return 0
    temp = CRT(inside_rems, mods) % prod_of_mods
    is_negative = temp < 0
    temp = abs(temp)
    t1 = prod_of_mods - temp
    if t1 < temp:
        temp = -t1
    if is_negative:
        temp *= -1
    return temp
