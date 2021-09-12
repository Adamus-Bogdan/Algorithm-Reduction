"""
This file contains class describing multivariable polynomial mapping.
"""
from sage.all import *


class Mapping:
    """
    Class describing n-variable polynomial mapping
    """

    def __init__(self, list_of_polynomials, name, list_of_primes, segre_constant, is_imaginary, ring=None):
        self.F = list_of_polynomials
        self.n = len(self.F)
        self.name = name
        if ring is None:
            self.R = self.F[0].parent()
        else:
            self.R = ring
        self.primes = list_of_primes
        self.r = segre_constant
        self.imaginary = is_imaginary

    @staticmethod
    def parse(list_of_string_definitions, name='F', field=QQ, list_of_primes=(3, 5, 7), segre_constant=1,
              params=dict({}), variables=None, is_imaginary=False):
        """
        method to parse input mapping from list of strings
        :param list_of_string_definitions: list of strings where each string describes one polynomial in mapping
        :param name: name of mapping
        :param field: mapping is defined over this field
        :param list_of_primes: set of prime numbers
        :param segre_constant: number used to clear denominators in Segre homotopy
        :param params: if mapping is parametrized one needs to put number values in place of parameters
        :param variables: name of variables in this mapping, if None defaults are used
        :param is_imaginary: flag if this mapping is defined over field with imaginary part
        """
        size = len(list_of_string_definitions)
        if variables is None:
            variables_out = [f'X{j+1}' for j in range(size)]
        else:
            variables_out = variables
        ring = PolynomialRing(field, variables_out)
        f_out = []
        for f in list_of_string_definitions:
            temp = ring("0")
            for m in str(expand(symbolic_expression(str(f).replace("I", "PLACEHOLDER")))).split("+"):
                temp += ring(Mapping.insert_params(str(m).replace("PLACEHOLDER", "I"), params))
            f_out.append(temp)
        return Mapping(f_out, name, list_of_primes, segre_constant, is_imaginary)

    def check_jacobian(self):
        """
        This method checks if determinant of Jacobi matrix is equal to 1
        :return: This method returns when det is equal to 1
        """
        jacobi_matrix = jacobian(self.F, self.R.gens())
        dj = det(jacobi_matrix)
        return dj == 1

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
        for index in range(self.n):
            result += f'{self.name}_{index+1} = {self.F[index]}\n'
        return result

    def check_inversion(self, inverse_candidate):
        """
        This method checks if mapping G is correct inverse of self
        :param inverse_candidate: object describing possible inverse
        :return: This method doesn't return any value - it raises an exception if G is not an inverse of self
        """
        for g, x in zip(inverse_candidate.F, self.R.gens()):
            res = g(self.F)
            if res == 0 or res/x not in CC:
                print("----------------------------")
                print(res)
                print("----------------------------")
                return False
        return True

    def segre_homotopy(self):
        """
        Function implements Segre homotopy
        :return: new mapping obtained using Segre homotopy
        """
        if self.R.base_ring() == QQ:
            field = ZZ
        else:
            field = GaussianIntegers()
        rr = self.R.change_ring(field)
        new_variables = [self.r * x for x in self.R.gens()]
        new_mapping = [f(new_variables) / self.r for f in self.F]
        return Mapping(new_mapping, str(self.r) + self.name, self.primes, 1, self.imaginary, rr)

    def reduce_mapping(self, p):
        """
        This function reduces polynomial mapping F modulo p
        :param p: prime number
        :return: new mapping - self reduced modulo p
        """
        zz = self.R.base_ring()
        new_field = zz.residue_field(zz(p))
        red = self.R.hom(self.R.change_ring(new_field))
        r_fp = [red(f) for f in self.F]
        return Mapping(r_fp, self.name+"_"+str(p), [], 1, self.imaginary)
