"""
This file contains at implementation of Groebner basis algorithm.
See details in README.md file.
"""
from sage.all import *
from mapping import Mapping
import subprocess
from tempfile import NamedTemporaryFile


def powers(ring, p):
    """
    For every monomial m = X1^a1 * ... * Xn^an we can calculate
    tuple (a1,...,an) containing powers of variables.
    This function calculates the tuple whose coordinates 
    are sums of corresponding coordinates in powers tuples defined
    for monomials in polynomial p
    :param ring: polynomial ring of polynomial p
    :param p: input polynomial
    :return: tuple with sums of variables powers
    """
    _powers = tuple([0] * len(ring.gens()))
    for m in p.monomials():
        _powers = tuple(a + b for a, b in zip(_powers, m.degrees()))
    return _powers


def check(ring, p, x):
    """
    This function checks if polynomial p can be polynomial G 
    for variable x
    :param ring: polynomial ring of polynomial p
    :param p: polynomial to verify if is coordinate of inversion
    :param x: variable to inverse
    :return:
    """
    index = ring.gens().index(x)
    pp = powers(ring, p)
    for j in range(int(len(ring.gens()) / 2)):
        if j != index:
            if pp[j] != 0:
                return False
        elif j == index:
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
    result = 0
    for m in polynomial.monomials():
        result += polynomial.monomial_coefficient(m) * m(x)
    return result


def find_basis_sage(ring, m):
    found_ideal = ring.ideal(m)
    return found_ideal.groebner_basis()


def find_basis_maple(ring, x, y, m, method=""):
    ch = ring.base_ring().characteristic()
    command = f"Groebner[Basis]({m}, lexdeg([{x}],[{y}])"
    if ch != 0:
        command += f", characteristic={ch}"
    if method != "":
        command += f", method={method}"
    command += ")"
    with NamedTemporaryFile() as f:
        f.write(bytes(command+";\n", "utf-8"))
        f.flush()
        c = subprocess.run(["maple", "-qt", f.name], capture_output=True)
        temp_list = c.stdout.decode().replace("\n", "").replace("\\", "")[1:-1].split(",")
        result = []
        for p in temp_list:
            r1 = ring("0")
            temp = (str(expand(symbolic_expression(p.strip().replace("I", "PLACEHOLDER"))))).split("+")
            for m in temp:
                r1 += ring(m.replace("PLACEHOLDER", "I"))
            result.append(r1)
        return result


def find_basis(ring, x, y, m, engine, method):
    if engine == "sage":
        return find_basis_sage(ring, m)
    else:
        return find_basis_maple(ring, x, y, m, method)

    
def algorithm(*, mapping, debug, engine="sage", method=""):
    """
    This function obtain an inverse of input polynomial mapping F
    :param mapping: Object of mapping that needs to be inverted
    :param debug: flag if debug should be printed to standard output
    :param engine: which engine should be used (available are: 'sage' and 'maple')
    :param method: which method of the engine should be used
    :return: polynomial mapping G = F^{-1}
    """
    if debug:
        print(str(mapping))
    # Step 1: create new polynomial ring with additional variables Y1, ..., Y_n
    old_names = [str(x) for x in mapping.R.gens()]
    new_names = [f"Y{index+1}" for index in range(mapping.n)]
    ring1 = PolynomialRing(mapping.R.base_ring(), old_names + new_names, order="lex")
    
    # Step 2: divide variables in new ring into "old ones" denoted by X
    #         and "new ones" denoted by Y
    y_vars = ring1.gens()[mapping.n:]
    x_vars = ring1.gens()[:mapping.n]
    temp = [y - f for y, f in zip(y_vars, mapping.F)]
    
    # Step 3: find the Groebner basis
    found_basis = find_basis(ring1, x_vars, y_vars, temp, engine, method)
    if debug:
        print("Groebner basis found")

    # Step 4: find inverse mapping polynomials in Groebner basis
    result = []
    for x in x_vars:
        found = False
        for b in found_basis:
            if check(ring1, b, x):
                g = x - b
                # Step 4.1: don't forget about changing ring
                #           for calculated mapping
                result.append(change_ring(ring1, mapping.R, g))
                found = True
                break
        assert found

    return Mapping(result, mapping.name+"^{-1}", [], 1, mapping.imaginary)
