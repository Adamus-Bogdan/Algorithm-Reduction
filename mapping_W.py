"""
This file contains a definition of mapping used in example 18 in the article:
"Algorithm for studying polynomial maps and reductions modulo prime number"
"""

from sage.all import *

R = PolynomialRing(QQ, ["X1", "X2", "X3", "X4"])
X1, X2, X3, X4 = R.gens()

e3 = 1
k3 = 1
m4 = 0
e4 = 1
g4 = 1
k4 = 1

F = [
    X1,
    X2 - QQ(1/3)*X1**3,
    X3 + X2**2*X4*g4**2 - X1*X2**2*e3 + X1*X2*X3*g4 - X2**3*k3 + X2**2*X3*m4 - X1**2*X2,
    X4 - X1*X2**2*e4 - X1*X2*X4*g4 - X2**3*k4 - X2**2*X4*m4 - X1**2*X3 - 2*X1*X2*X3*m4/g4 - X2**2*X3*m4**2/g4**2 
]