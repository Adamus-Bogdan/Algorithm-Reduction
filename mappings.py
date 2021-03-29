"""
This file contains a definition of mappings used as examples in the article:
"Algorithm for studying polynomial maps and reductions modulo prime number"
"""
from sage.all import *

from mapping import Mapping

mappings = {}

# Mapping presented in example 17 in the article
# "Algorithm for studying polynomial maps and reductions modulo prime number"
f = Mapping([
    "X1",
    "1/3*X1**3 + X2",
    "-1/243*X1**15 - 2/81*X1**13 - 5/81*X1**12*X2 - 1/27*X1**11 - 8/27*X1**10*X2 - 10/27*X1**9*X2**2" +
    "- 2/27*X1**9 - 1/3*X1**8*X2 - 4/3*X1**7*X2**2 - 10/9*X1**6*X2**3 + 1/9*X1**7 - 1/3*X1**6*X2 - X1**5*X2**2" +
    "- 8/3*X1**4*X2**3 - 5/3*X1**3*X2**4 - 1/9*X1**6*X4 + 1/3*X1**5 + 2/3*X1**4*X2 - X1**2*X2**3 - 2*X1*X2**4" +
    "- X2**5 - 1/3*X1**4*X3 - 2/3*X1**3*X2*X4 + X1**2*X2 + X1*X2**2 + X2**3 - X1*X2*X3 - X2**2*X4 + X3",
    "1/81*X1**13 + 2/27*X1**11 + 4/27*X1**10*X2 + 4/27*X1**9 + 2/3*X1**8*X2 + 2/3*X1**7*X2**2 + 4/9*X1**7" +
    "+ X1**6*X2 + 2*X1**5*X2**2 + 4/3*X1**4*X2**3 + 5/3*X1**4*X2 + 2*X1**3*X2**2 + 2*X1**2*X2**3" +
    "+ X1*X2**4 + 1/3*X1**4*X4 + X1*X2**2 + X2**3 + X1**2*X3 + X1*X2*X4 + X4"
],
    name="EX17",
    r=243,
    primes=[3, 5, 7, 11, 13, 17, 19])
mappings[f.name] = f


# Mapping presented in example 19 in the article
# "Algorithm for studying polynomial maps and reductions modulo prime number"
R = PolynomialRing(GaussianIntegers().fraction_field(), ["X1", "X2", "X3", "X4", "X5"], 5)
g = R("(((X4+I*X5)^2-1)*X1+(2*(X4+I*X5))*X2+I*((X4+I*X5)^2+1)*X3)*((2*(X4+I*X5))*X1-((X4+I*X5)^2-1)*X2)")
H = g.gradient()
F = [str(x + h) for x, h in zip(R.gens(), H)]
g = Mapping(F, name="EX19", field=R.base_ring(), primes=[3, 7, 11, 19, 23], imaginary=True)
mappings[g.name] = g


# Mapping presented in example 20 in the article
# "Algorithm for studying polynomial maps and reductions modulo prime number"
f = Mapping([
    "X1",
    "X2 + (b1*X1 + (b3+2*b5+b7)*X3 + 3*b3*X6 + (2*b4+b7)*X7 + b4*X4 + b5*X5)^3",
    "X3 - 3*(f1*X1 + (f3+f7)*X3 + 3*f3*X6 + (2*f4 + f7)*X7 + f4*X4)^3",
    "X4 + (d1*X1 + (d3+d7)*X3 + 3*d3*X6 + d7*X7)^3 - 6*(f1*X1 + (f3+f7)*X3 + 3*f3*X6 + (2*f4+f7)*X7 + f4*X4)^3",
    "X5 + (e1*X1 + (e3+e7)*X3 + 3*e3*X6 + e7*X7)^3 + 6*(f1*X1 + (f3+f7)*X3 + 3*f3*X6 + (2*f4+f7)*X7 + f4*X4)^3",
    "X6 + (f1*X1 + (f3+f7)*X3 + 3*f3*X6 + (2*f4+f7)*X7 + f4*X4)^3",
    "X7 + 3*(f1*X1 + (f3+f7)*X3 + 3*f3*X6 + (2*f4+f7)*X7 + f4*X4)^3",
    "X8 + (h1*X1 + (h3 + 2*h5 + h7)*X3 + 3*h3*X6 + (2*h4+h7)*X7 + h4*X4 + h5*X5)^3"
],
    name="EX20",
    r=1,
    primes=[3, 5, 7, 7103, 10937, 9461],
    imaginary=True,
    params={
            "b1": "3", "b3": "2", "b4": "1", "b5": "1", "b7": "1",
            "f1": "5", "f3": "2", "f4": "1", "f7": "1",
            "d1": "1", "d3": "3", "d7": "3",
            "e1": "1", "e3": "7", "e7": "1",
            "h1": "3", "h3": "1", "h4": "7", "h5": "1", "h7": "1",
        }
)
mappings[f.name] = f

