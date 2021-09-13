"""
This file contains a definition of couple of mappings used during working on the article:
"Algorithm for studying polynomial maps and reductions modulo prime number"
"""
from sage.all import *

from mapping import Mapping

mappings = {}

'''
The following 8 mappings were defined by Hubbers in his master's thesis. See [5] in README.md file
'''
h = Mapping.parse([
    "X1",
    "X2",
    "X3",
    "X4 - a4*X1^3 - b4*X1^2*X2 - c4*X1^2*X3 - e4*X1*X2^2 - f4*X1*X2*X3" +
    "- h4*X1*X3^2 - k4*X2^3 - l4*X2^2*X3 - n4*X2*X3^2 - q4*X3^3"
],
    name="H1",
    params={"a4": "1", "b4": "1", "c4": "1", "e4": "1", "f4": "1",
            "h4": "1", "k4": "1", "l4": "1", "n4": "1", "q4": "1"})
mappings[h.name] = h


h = Mapping.parse([
    "X1",
    "X2 - 1/3*X1^3 - h2*X1*X3**2 - q2*X3**3",
    "X3",
    "X4 - X1**2 - h4*X1*X3**2 - q4*X3**3"
],
    name="H2",
    params={"h2": "1", "q2": "1", "h4": "1", "q4": "1"},
    segre_constant=3)
mappings[h.name] = h


h = Mapping.parse([
    "X1",
    "X2 - 1/3*X1^3 - c1*X1^2*X4 + 3*c1*X1*X2*X3 - (16*q4*c1^2-r4^2)/48/c1^2*X1*X3^2" +
    "- 1/2*r4*X1*X3*X4 + 3/4*r4*X2*X3^2 - r4*q4/12/c1*X3^3 - r4^2/16/c1*X3^2*X4",
    "X3",
    "X4 -X1^2*X3 + r4/4/c1*X1*X3^2 - 3*c1*X1*X3*X4 + 9*c1*X2*X3^2 - q4*X3^3 - 3/4*r4*X3^2*X4"
],
    name="H3",
    params={"c1": "1", "q4": "1", "r4": "1"},
    segre_constant=48,
    list_of_primes=[3, 5, 7, 11, 13, 17])
mappings[h.name] = h


h = Mapping.parse([
    "X1",
    "X2 - 1/3*X1^3",
    "X3 - X1^2*X2 - e3*X1*X2^2 -k3*X2^3",
    "X4 - e4*X1*X2^2 - k4*X2^3"
],
    name="H4",
    params={"e3": "1", "k3": "1", "e4": "1", "k4": "1"},
    segre_constant=3,
    list_of_primes=[3, 5, 7, 11, 13])
mappings[h.name] = h


h = Mapping.parse([
    "X1",
    "X2 - 1/3*X1^3 + i3*X1*X2*X4 - j2*X1*X4^2 + s3*X2*X4^2 + i3^2*X3*X4^2 - t2*X4^3",
    "X3 - X1^2*X2 - 2*s3/i3*X1*X2*X4 - i3*X1*X3*X4 - j3*X1*X4^2 - s3^2/i3^2*X2*X4^2 - s3*X3*X4^2 - t3*X4^3",
    "X4"
],
    name="H5",
    params={"i3": "1", "j2": "1", "s3": "1", "t2": "1", "t3": "1", "j3": "1"},
    segre_constant=3,
    list_of_primes=[3, 5, 7, 11, 13])
mappings[h.name] = h


h = Mapping.parse([
    "X1",
    "X2 - 1/3*X1^3 - j2*X1*X4^2 - t2*X4^3",
    "X3 - X1^2*X2 - e3*X1*X2^2 - g3*X1*X2*X4 - j3*X1*X4^2 - k3*X2^3 - m3*X2^2*X4",
    "X4"
],
    name="H6",
    params={"j2": "1", "t2": "1", "e3": "1", "g3": "1", "j3": "1", "k3": "1", "m3": "1"},
    segre_constant=3,
    list_of_primes=[5, 7, 11, 13, 17])
mappings[h.name] = h


h = Mapping.parse([
    "X1",
    "X2-(1/3)*X1^3",
    "-X1*X2^2*e3-X2^3*k3-X1^2*X2+X3",
    "-X1*X2^2*e4-X1*X2*X3*f4-X1*X3^2*h4-X2^3*k4-X2^2*X3*l4-X2*X3^2*n4-X3^3*q4-X1^2*X3+X4"
],
    name="H7",
    params={"e3": "1", "k3": "1", "e4": "1", "f4": "1", "h4": "1", "k4": "1", "l4": "1", "n4": "1", "q4": "1"},
    segre_constant=3,
    list_of_primes=[5, 7, 11, 13, 17, 23, 29, 31, 37])
mappings[h.name] = h


h = Mapping.parse([
    "X1",
    "X2-(1/3)*X1^3",
    "X2^2*X4*g4^2-X1*X2^2*e3+X1*X2*X3*g4-X2^3*k3+X2^2*X3*m4-X1^2*X2+X3",
    "X4-X1^2*X3-e4*X1*X2^2-2*m4*X1*X2*X3/g4-g4*X1*X2*X4-k4*X2^3-m4^2*X2^2*X3/g4^2-m4*X2^2*X4"
],
    name="H8",
    params={"g4": "1", "e3": "1", "k3": "1", "m4": "1", "e4": "1", "k4": "1"},
    segre_constant=3,
    list_of_primes=[5, 7, 11, 13, 17, 19, 23])
mappings[h.name] = h


'''
The following 6 mappings were defined by de Bondt in his book. See [6] in README.md file
'''
R1 = PolynomialRing(GaussianIntegers().fraction_field(), ["X1", "X2", "X3", "X4", "X5"], 5)
g1 = R1("(((X4+I*X5)^2-1)*X1+(2*(X4+I*X5))*X2+I*((X4+I*X5)^2+1)*X3)^2")
H = g1.gradient()
F = [x + h for x, h in zip(R1.gens(), H)]
g = Mapping(F, name="B1", list_of_primes=[3, 7, 11, 47], segre_constant=1, is_imaginary=True)
mappings[g.name] = g


R2 = PolynomialRing(GaussianIntegers().fraction_field(), ["X1", "X2", "X3", "X4", "X5"], 5)
g2 = R2("(((X4+I*X5)^2-1)*X1+(2*(X4+I*X5))*X2+I*((X4+I*X5)^2+1)*X3)*((2*(X4+I*X5))*X1-((X4+I*X5)^2-1)*X2)")
H = g2.gradient()
F = [x + h for x, h in zip(R2.gens(), H)]
g = Mapping(F, name="B2", list_of_primes=[3, 7, 11, 19, 23], segre_constant=1, is_imaginary=True)
mappings[g.name] = g


R3 = PolynomialRing(GaussianIntegers().fraction_field(), ["X1", "X2", "X3", "X4", "X5", "X6", "X7"], 7)
g3 = R3("(((X4+I*X5)^2-(X6+I*X7)^2)*X1+(2*(X4+I*X5))*(X6+I*X7)*X2+I*((X4+I*X5)^2+(X6+I*X7)^2)*X3)^2")
H = g3.gradient()
F = [x + h for x, h in zip(R3.gens(), H)]
g = Mapping(F, name="B3", list_of_primes=[3, 7, 11, 19, 23], segre_constant=1, is_imaginary=True)
mappings[g.name] = g


R4 = PolynomialRing(GaussianIntegers().fraction_field(), ["X1", "X2", "X3", "X4", "X5", "X6", "X7"], 7)
g4 = R4("(((X4+I*X5)^2-(X6+I*X7)^2)*X1+(2*(X4+I*X5))*(X6+I*X7)*X2+I*((X4+I*X5)^2+(X6+I*X7)^2)*X3)*" +
        "((2*(X4+I*X5))*(X6+I*X7)*X1-((X4+I*X5)^2-(X6+I*X7)^2)*X2)")
H = g4.gradient()
F = [x + h for x, h in zip(R4.gens(), H)]
g = Mapping(F, name="B4", list_of_primes=[3, 7, 11, 19, 23], segre_constant=1, is_imaginary=True)
mappings[g.name] = g


R5 = PolynomialRing(GaussianIntegers().fraction_field(), ["X1", "X2", "X3", "X4", "X5", "X6", "X7"], 7)
g3 = R5("(((X4+I*X5)^2-(X6+I*X7)^2)*X1+(2*(X4+I*X5))*(X6+I*X7)*X2+I*((X4+I*X5)^2+(X6+I*X7)^2)*X3)^2")
g5 = g3 + R5("(X6+I*X7)^5*X4")
H = g5.gradient()
F = [x + h for x, h in zip(R5.gens(), H)]
g = Mapping(F, name="B5", list_of_primes=[3, 7, 11, 19, 23], segre_constant=1, is_imaginary=True)
mappings[g.name] = g


R6 = PolynomialRing(GaussianIntegers().fraction_field(), ["X1", "X2", "X3", "X4", "X5", "X6", "X7"], 7)
g4 = R6("(((X4+I*X5)^2-(X6+I*X7)^2)*X1+(2*(X4+I*X5))*(X6+I*X7)*X2+I*((X4+I*X5)^2+(X6+I*X7)^2)*X3)" +
        "*((2*(X4+I*X5))*(X6+I*X7)*X1-((X4+I*X5)^2-(X6+I*X7)^2)*X2)")
g6 = g4 + R6("(X6+I*X7)^5*X4")
H = g6.gradient()
F = [x + h for x, h in zip(R6.gens(), H)]
g = Mapping(F, name="B6", list_of_primes=[3, 7, 11, 19, 23], segre_constant=1, is_imaginary=True)
mappings[g.name] = g


# Mapping presented in example 17 in the article
# "Algorithm for studying polynomial maps and reductions modulo prime number"
f = Mapping.parse([
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
    segre_constant=243,
    list_of_primes=[3, 5, 7, 11, 13, 17, 19])
mappings[f.name] = f


# Mapping presented in example 19 in the article
# "Algorithm for studying polynomial maps and reductions modulo prime number"
ex00 = Mapping.parse([
    "X1+I*(X8^3)",
    "X2+(2*X1+5*X6+7*X7+11*X8)^3",
    "X3+(13*X1+19*X6+23*X7+29*X8)^3",
    "X4+(31*X1+41*X6+43*X7+47*X8)^3",
    "X5+(53*X1)^3",
    "X6",
    "X7+(59*X1+61*X8)^3",
    "X8+I*X6^3",
    "X9+(67*X1+71*X5+73*X6+79*X7+83*X8)^3"
],
    segre_constant=1,
    name="EX19",
    is_imaginary=True,
    field=GaussianIntegers().fraction_field(),
    list_of_primes=[530560271, 530560211, 530560207, 530560183])
mappings[ex00.name] = ex00


# Mapping presented in example 20 in the article
# "Algorithm for studying polynomial maps and reductions modulo prime number"
R = PolynomialRing(GaussianIntegers().fraction_field(), ["X1", "X2", "X3", "X4", "X5"], 5)
g = R("(((X4+I*X5)^2-1)*X1+(2*(X4+I*X5))*X2+I*((X4+I*X5)^2+1)*X3)*((2*(X4+I*X5))*X1-((X4+I*X5)^2-1)*X2)")
H = g.gradient()
F = [x + h for x, h in zip(R.gens(), H)]
g = Mapping(F, "EX20", R, [3, 7, 11, 19, 23], 1, True)
mappings[g.name] = g
