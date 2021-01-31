"""
This file contains a definition of mapping used in example 17 in the article:
"Algorithm for studying polynomial maps and reductions modulo prime number"
"""

from sage.all import *


class Mapping:
    def __init__(self, F, name='F', field=QQ, primes=[3,5,7], r=1, params={}, variables=None):
        self.n = len(F)
        self.name = name
        if variables is None:
            self.variables = ['X{0}'.format(i) for i in range(1, self.n+1)]
        else:
            self.variables = variables
        self.R = PolynomialRing(field, self.variables)
        self.F = [self.R(self.replace(str(f), params)) for f in F]
        self.primes = primes
        self.r = r


    def replace(self, s, d):
        result = s
        for k in d:
            result = result.replace(k, d[k])
        return result

    
    def __str__(self):
        result = '==================== Mapping ====================\n'
        result += str(self.R) + '\n'
        for i in range(self.n):
            result += '{0}_{1} = {2}\n'.format(self.name, i+1, self.F[i])
        return result

    
    def check_inversion(self, G):
        for g, x in zip(G, self.R.gens()):
            assert g(self.F) == x


    def segre_homotopy(self):
        """
        Function implements Segre homotopy
        :param F: Polynomial mapping defined over ring R
        :param R: ring
        :param r: chosen element r
        :return: Function translated using Segre homotopy
        """
        n_X = [self.r*x for x in self.R.gens()]
        new_F = [f(n_X)/self.r for f in self.F]
        return Mapping(new_F, name=str(self.r) + self.name, field=self.R.base_ring(), primes=self.primes, r=1,
                variables = [str(v) for v in self.variables])

    def reduce_mapping(self,p):
        """
        This function reduces polynomial mapping F modulo prime number p
        :param F: Polynomial mapping defined over ring R
        :param p: prime number
        :return: reduced modulo p polynomial mapping
        """
        var_names = ['X{0}'.format(i+1) for i in range(len(self.F))]
        if is_prime(p):
            field = GF(p)
        else:
            field = IntegerModRing(p)
        rFp = [str(f) for f in self.F]
        return Mapping(rFp, name=self.name+"_"+str(p), field=field, primes=[], r=1, variables=var_names)


mappings = {}


h = Mapping([
     "X1",
     "X2",
     "X3",
     "X4 - a4*X1^3 - b4*X1^2*X2 - c4*X1^2*X3 - e4*X1*X2^2 - f4*X1*X2*X3 - h4*X1*X3^2 - k4*X2^3 - l4*X2^2*X3 - n4*X2*X3^2 - q4*X3^3"        
     ], name="H4_1", params={"a4": "1", "b4": "1", "c4": "1", "e4": "1", "f4": "1", "h4": "1", "k4": "1", "l4": "1", "n4": "1", "q4": "1"})

mappings[h.name] = h


h = Mapping([
       "X1",
       "X2 - 1/3*X1^3 - h2*X1*X3**2 - q2*X3**3",
       "X3",
       "X4 - X1**2 - h4*X1*X3**2 - q4*X3**3"
    ], name="H4_2", params={"h2": "1", "q2": "1", "h4": "1", "q4": "1"}, r=3)

mappings[h.name] = h

h = Mapping([
        "X1",
        "X2 - 1/3*X1^3 - c1*X1^2*X4 + 3*c1*X1*X2*X3 - (16*q4*c1^2-r4^2)/48/c1^2*X1*X3^2 - 1/2*r4*X1*X3*X4 + 3/4*r4*X2*X3^2 - r4*q4/12/c1*X3^3 - r4^2/16/c1*X3^2*X4",
        "X3",
        "X4 -X1^2*X3 + r4/4/c1*X1*X3^2 - 3*c1*X1*X3*X4 + 9*c1*X2*X3^2 - q4*X3^3 - 3/4*r4*X3^2*X4"
        ], name="H4_3", params={"c1": "1", "q4": "1", "r4": "1"}, r=48, primes=[3,5,7,11,13,17])

mappings[h.name] = h


h = Mapping([
        "X1",
        "X2 - 1/3*X1^3",
        "X3 - X1^2*X2 - e3*X1*X2^2 -k3*X2^3",
        "X4 - e4*X1*X2^2 - k4*X2^3"
    ], name="H4_4", params={"e3": "1", "k3": "1", "e4": "1", "k4": "1"}, r=3, primes=[3,5,7,11,13]) 

mappings[h.name] = h


h = Mapping([
        "X1",
        "X2 - 1/3*X1^3 + i3*X1*X2*X4 - j2*X1*X4^2 + s3*X2*X4^2 + i3^2*X3*X4^2 - t2*X4^3",
        "X3 - X1^2*X2 - 2*s3/i3*X1*X2*X4 - i3*X1*X3*X4 - j3*X1*X4^2 - s3^2/i3^2*X2*X4^2 - s3*X3*X4^2 - t3*X4^3",
        "X4"
        ], name="H4_5", params={"i3": "1", "j2": "1", "s3": "1", "t2": "1", "t3": "1", "j3": "1"}, r=3,
        primes=[3,5,7,11,13])
mappings[h.name] = h


h = Mapping([
        "X1",
        "X2 - 1/3*X1^3 - j2*X1*X4^2 - t2*X4^3",
        "X3 - X1^2*X2 - e3*X1*X2^2 - g3*X1*X2*X4 - j3*X1*X4^2 - k3*X2^3 - m3*X2^2*X4",
        "X4"
        ], name="H4_6", params={"j2": "1", "t2": "1", "e3": "1", "g3": "1", "j3": "1", "k3": "1", "m3": "1"}, r=3, primes=[5,7,11,13,17])
mappings[h.name] = h



h = Mapping([
        "X1",
        "X2-(1/3)*X1^3",
        "-X1*X2^2*e3-X2^3*k3-X1^2*X2+X3",
        "-X1*X2^2*e4-X1*X2*X3*f4-X1*X3^2*h4-X2^3*k4-X2^2*X3*l4-X2*X3^2*n4-X3^3*q4-X1^2*X3+X4"
        ], name="H4_7", params={"e3": "1", "k3": "1", "e4": "1", "f4": "1", "h4": "1", "k4": "1", "l4": "1", "n4": "1", "q4": "1"}, r=3, primes=[5,7,11,13,17,23,29,31,37])
mappings[h.name] = h


h = Mapping([
         "X1", 
         "X2-(1/3)*X1^3", 
         "X2^2*X4*g4^2-X1*X2^2*e3+X1*X2*X3*g4-X2^3*k3+X2^2*X3*m4-X1^2*X2+X3", 
         "X4-X1^2*X3-e4*X1*X2^2-2*m4*X1*X2*X3/g4-g4*X1*X2*X4-k4*X2^3-m4^2*X2^2*X3/g4^2-m4*X2^2*X4"        
         ], name="H4_8", params={"g4": "1", "e3": "1", "k3": "1", "m4": "1", "e4": "1", "k4": "1"}, r=3, primes=[5,7,11,13,17,19])
mappings[h.name] = h


f = Mapping([
        "X1",
        "1/3*X1**3 + X2",
        "-1/243*X1**15 - 2/81*X1**13 - 5/81*X1**12*X2 - 1/27*X1**11 - 8/27*X1**10*X2 - 10/27*X1**9*X2**2 - 2/27*X1**9 - 1/3*X1**8*X2 - 4/3*X1**7*X2**2 - 10/9*X1**6*X2**3 + 1/9*X1**7 - 1/3*X1**6*X2 - X1**5*X2**2 - 8/3*X1**4*X2**3 - 5/3*X1**3*X2**4 - 1/9*X1**6*X4 + 1/3*X1**5 + 2/3*X1**4*X2 - X1**2*X2**3 - 2*X1*X2**4 - X2**5 - 1/3*X1**4*X3 - 2/3*X1**3*X2*X4 + X1**2*X2 + X1*X2**2 + X2**3 - X1*X2*X3 - X2**2*X4 + X3",
        "1/81*X1**13 + 2/27*X1**11 + 4/27*X1**10*X2 + 4/27*X1**9 + 2/3*X1**8*X2 + 2/3*X1**7*X2**2 + 4/9*X1**7 + X1**6*X2 + 2*X1**5*X2**2 + 4/3*X1**4*X2**3 + 5/3*X1**4*X2 + 2*X1**3*X2**2 + 2*X1**2*X2**3 + X1*X2**4 + 1/3*X1**4*X4 + X1*X2**2 + X2**3 + X1**2*X3 + X1*X2*X4 + X4"
    ], name="EX17", r=81, primes=[5,7,11])
mappings[f.name] = f

R = PolynomialRing(QQ,["X1", "X2", "X3", "X4", "X5"])
X = X1, X2, X3, X4, X5 = R.gens()
g1 = R("(((X4+X5)^2-1)*X1+(2*(X4+X5))*X2+((X4+X5)^2+1)*X3)^2")
H = g1.gradient()
F = [x + h for x,h in zip(X,H)]
g = Mapping([str(f) for f in F], name="G1")

mappings[g.name] = g

n = Mapping(['X1 + (X1**d1 + X2)**d2', 'X2 + X1**d1'], name="N", params={"d1": "3", "d2": "4"}, primes=[3,5,7,11,13,17,19])
mappings[n.name] = n


n = Mapping(["X1 + (X1**d2 + X2)**d1", "X2 + (X1*X3)**d2", "X3 + (X1*X2 + X2*X3)**d3"], name="N3", params={"d1": "2", "d2": "2", "d3": "1"}, primes=[3,5,7,11,13,17,19,23,29,31,37,41,47,53])
mappings[n.name] = n

n = Mapping([
        "X1 + (X1**d2 + X2)**d1",
        "X2 + X1**d2",
        "X3 + (X3*X4)**d3",
        "X4 + X3**d4",
        "X5 + (X1*X3 + X2*X4)**d5"
        ], name="N5_1", params={"d1": "2", "d2": "3", "d3": "2", "d4": "2", "d5": "2"})
mappings[n.name] = n


n = Mapping([
        "X1 + (X1**d2 + X2)**d1",
        "X2 + X1**d2",
        "X3 + (X3*X4)**d3",
        "X4 + X3**d4",
        "X5 + (X1*X3 + X2*X4)**d5"
        ], name="N5_2", params={"d1": "2", "d2": "3", "d3": "1", "d4": "2", "d5": "1"})
mappings[n.name] = n

v = Mapping([
        str(expand(symbolic_expression("X1+(X8)**3"))),
        str(expand(symbolic_expression("X2+(X1-X3+2*X4-X5+12*X6+X7)**3"))),
        str(expand(symbolic_expression("X3-3*(10*X3/(3**(1/3))+4*X4/(3**(1/3))+9*X6/(3**(1/3))+15*X7/(3**(1/3)))**3"))),
        str(expand(symbolic_expression("X4-6*(10*X3/(3**(1/3))+4*X4/(3**(1/3))+9*X6/(3**(1/3))+15*X7/(3**(1/3)))**3"))),
        str(expand(symbolic_expression("X5+6*(20*X3/(3**(1/3))+4*X4/(3**(1/3))+9*X6/(3**(1/3))+15*X7/(3**(1/3)))**3"))),
        str(expand(symbolic_expression("X6+(10*X3/(3**(1/3))+4*X4/(3**(1/3))+9*X6/(3**(1/3))+15*X7/(3**(1/3)))**3"))),
        str(expand(symbolic_expression("X7+3*(10*X3/(3**(1/3))+4*X4/(3**(1/3))+9*X6/(3**(1/3))+15*X7/(3**(1/3)))**3"))),
        str(expand(symbolic_expression("X8+(X3+X4+X5+X6+X7)**3")))
        ], name="B8", primes=[5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 47])
mappings[v.name] = v



names = [
            "H4_1",
            "H4_2",
            "H4_3",
            "H4_4",
            "H4_5",
            "H4_6",
            "H4_7",
            "H4_8",
            "EX17"
        ]

