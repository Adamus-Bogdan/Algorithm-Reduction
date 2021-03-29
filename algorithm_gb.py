"""
This file contains at implementation of Groebner basis algorithm.
See details in README.md file.
"""
from sage.all import *
from mapping import Mapping


def powers(R, p):
    """
    For every monomial m = X1^a1 * ... * Xn^an we can calculate
    tuple (a1,...,an) containing powers of variables.
    This function calculates the tuple whose coordinates 
    are sums of corresponding coordinates in powers tuples defined
    for monomials in polynomial p
    :param R: polynomial ring of polynomial p
    :param p: input polynomial
    :return: tuple with sums of variables powers
    """
    _powers = tuple([0] * len(R.gens()))
    for m in p.monomials():
        _powers = tuple(a + b for a, b in zip(_powers, m.degrees()))
    return _powers


def check(R, p, x):
    """
    This function checks if polynomial p can be polynomial G 
    for variable x
    :param R: polynomial ring of polynomial p
    :param p: polynomial to verify if is coordinate of inversion
    :param x: variable to inverse
    :return:
    """
    i = R.gens().index(x)
    pp = powers(R, p)
    for j in range(int(len(R.gens()) / 2)):
        if j != i:
            if pp[j] != 0:
                return False
        elif j == i:
            if pp[j] != 1:
                return False
    return True


def change_ring(old_ring, new_ring, polynomial):
    """
    This function change ring (from bigger one with additional variables
    into smaller one) of provided polynomial
    :param old_ring: bigger polynomial ring in X1,...,Xn,Y1,...,Yn
    :param new_ring: smaller polynomial ring in X1,...,Xn
    :param polynomial: polynomial defined in X1,...,Xn,Y1,...,Yn
    :return: the polynomial defined in X1,...,Xn
    """
    assert len(old_ring.gens()) == 2 * len(new_ring.gens())
    x = [0]*len(new_ring.gens()) + list(new_ring.gens())
    return polynomial(x)


def algorithm(mapping, debug):
    """
    This function obtain an inverse of input polynomial mapping F
    :param mapping: Object of mapping that needs to be inverted
    :param debug: flag if debug should be printed to standard output
    :return: polynomial mapping G = F^{-1}
    """
    if debug:
        print(str(mapping))
    # Step 1: create new polynomial ring with additional variables Y1, ..., Y_n
    old_names = [str(x) for x in mapping.R.gens()]
    new_names = [f"Y{i+1}" for i in range(mapping.n)]
    R1 = PolynomialRing(mapping.R.base_ring(), old_names + new_names, order="lex")
    
    # Step 2: divide variables in new ring into "old ones" denoted by X
    #         and "new ones" denoted by Y
    Y = R1.gens()[mapping.n:]
    X = R1.gens()[:mapping.n]

    # Step 3: create ideal for polynomials with new variable added
    ideal = R1.ideal([y - f for y, f in zip(Y, mapping.F)])
    
    # Step 4: find the Groebner basis of previously defined ideal
    B = ideal.groebner_basis()
    if debug:
        print("Groebner basis found")

    # Step 5: find inverse mapping polynomials in Groebner basis
    G = []
    for x in X:
        found = False
        for b in B:
            if check(R1, b, x):
                g = x - b
                # Step 5.1: don't forget about changing ring
                #           for calculated mapping
                G.append(change_ring(R1, mapping.R, g))
                found = True
                break
        assert found

    return Mapping(G, name=mapping.name+"^{-1}", field=mapping.R.base_ring(),
                   imaginary=mapping.imaginary, r=1)
