"""
This file contains class describing multivariable polynomial mapping.
"""
from sage.all import *


class Mapping:
    """
    Class describing n-variable polynomial mapping
    """
    def __init__(self, F, name='F', field=QQ, primes=(3, 5, 7), r=1, params=dict({}), variables=None, imaginary=False):
        """
        Constructor
        :param F: list of strings where each string describes one polynomial in mapping
        :param name: name of mapping
        :param field: mapping is defined over this field
        :param primes: set of prime numbers
        :param r: number used to clear denominators in Segre homotopy
        :param params: if mapping is parametrized one needs to put number values in place of parameters
        :param variables: name of variables in this mapping, if None defaults are used
        :param imaginary: flag if this mapping is defined over field with imaginary part
        """
        self.n = len(F)
        self.name = name
        if variables is None:
            self.variables = [f'X{i+1}' for i in range(self.n)]
        else:
            self.variables = variables
        self.R = PolynomialRing(field, self.variables)
        self.F = [self.R(Mapping.insert_params(str(f), params)) for f in F]
        self.primes = primes
        self.r = r
        self.imaginary = imaginary

    def check_jacobian(self):
        """
        This method checks if determinant of Jacobi matrix is equal to 1
        :return: This method doesn't return any value - it raises an exception if determinant is not equal to 1
        """
        J = jacobian(self.F, self.R.gens())
        dj = det(J)
        assert dj == 1

    @staticmethod
    def insert_params(s, d):
        """
        This static method is used to insert values of parameters into polynomials in the mapping
        :param s: string containing definition of polynomial
        :param d: dictionary containing values of parameters
        :return:
        """
        result = s
        for k in d:
            result = result.replace(k, d[k])
        return result

    def __str__(self):
        """
        Standard method to get string representation of the mapping
        :return:
        """
        result = '==================== Mapping ====================\n'
        result += str(self.R) + '\n'
        for i in range(self.n):
            result += f'{self.name}_{i+1} = {self.F[i]}\n'
        return result

    def check_inversion(self, G):
        """
        This method checks if mapping G is correct inverse of self
        :param G: object describing possible inverse
        :return: This method doesn't return any value - it raises an exception if G is not an inverse of self
        """
        for g, x in zip(G.F, self.R.gens()):
            assert g(self.F) == x

    def segre_homotopy(self):
        """
        Function implements Segre homotopy
        :return: new mapping obtained using Segre homotopy
        """
        if self.R.base_ring() == QQ:
            field = ZZ
        else:
            field = GaussianIntegers()
        n_X = [self.r * x for x in self.R.gens()]
        new_F = [f(n_X) / self.r for f in self.F]
        return Mapping(new_F, name=str(self.r) + self.name, field=field, primes=self.primes, r=1,
                       variables=[str(v) for v in self.variables], imaginary=self.imaginary)

    def reduce_mapping(self, p):
        """
        This function reduces polynomial mapping F modulo p
        :param p: prime number
        :return: new mapping - self reduced modulo p
        """
        zz = self.R.base_ring()
        new_field = zz.residue_field(prime=zz(p))
        red = self.R.hom(self.R.change_ring(new_field))
        rFp = [red(f) for f in self.F]
        m = Mapping(["0"]*self.n)
        m.F = rFp
        m.n = self.n
        m.R = m.F[0].parent()
        m.name = self.name+"_"+str(p)
        m.primes = []
        m.r = 1
        m.imaginary = self.imaginary
        return m
