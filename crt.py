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
        return {(index, m.degrees()): [zz(c)] for index, f in enumerate(mapping)
                for m, c in zip(f.monomials(), f.coefficients())}
    else:
        return {(index, m.degrees()): [tuple((p, zz(c)))] for index, f in enumerate(mapping)
                for m, c in zip(f.monomials(), f.coefficients())}


def get_monomial(ring, a):
    """
    Function is used to transform tuple of exponents to monomial
    :param ring: ring
    :param a: tuple of exponents
    :return:
    """
    result = ring("1")
    for x, p in zip(ring.gens(), a):
        result *= x**p
    return result


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
        f[index] += mapping.R(str(x))*get_monomial(mapping.R, k)
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


# Extended Euclides Algorithm
# this function was copied from:
# https://ask.sagemath.org/question/44287/solving-systems-of-congruences-with-gaussian-integers/
def extended_euclides(a, b, my_quo):
    r0 = a
    r1 = b
    s0 = 1
    s1 = 0
    t0 = 0
    t1 = 1

    while r1 != 0:
        q = my_quo(r0, r1)
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1

    return r0, s0, t0


# Chinese Reminder Theorem
# this function was copied from:
# https://ask.sagemath.org/question/44287/solving-systems-of-congruences-with-gaussian-integers/
def chinese_remainder(remainders, modules, my_quo):
    m = reduce(lambda x, y: x*y, modules)
    c = 0
    for v_i, m_i in zip(remainders, modules):
        m_div_m_i = my_quo(m, m_i)
        _, s_i, _ = extended_euclides(m_div_m_i, m_i, my_quo)
        a = v_i * s_i; b = m_i
        c_i = a - my_quo(a, b) * b

        c += c_i * m_div_m_i
    return c


def my_crt(input_dictionary, mapping):
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
    :param mapping: polynomial ring of resulting mapping
    :return: Dictionary in form { (i, a) => c }
    """
    result = {}
    for k in input_dictionary:
        mods = [t[0] for t in input_dictionary[k]]
        rems = [t[1] for t in input_dictionary[k]]
        prod_of_mods = reduce(lambda x, y: x*y, mods)

        if mapping.imaginary:
            def _quo(a, b):
                return GaussianIntegers()(int(real(a/b)) + I*int(imag(a/b)))

            def _rem(a, b):
                return a - _quo(a, b)*b
        else:
            def _quo(a, b):
                return a//b

            def _rem(a, b):
                return a % b

        temp = chinese_remainder(rems, mods, _quo)
        temp = _rem(temp, prod_of_mods)
        t1 = prod_of_mods - temp
        if t1 < temp:
            temp = -t1
        result[k] = temp
    return result
