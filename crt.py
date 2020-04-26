import sys
from sage.all import *
from functools import reduce

def map2dict(F, p=None):
    D = {}
    for i, f in enumerate(F):
        for k in f.dict():
            if p is None:
                D[(i,k)] = [int(f.dict()[k])]
            else:
                v1 = int(f.dict()[k])
                v2 = -(p-v1)
                if abs(v1) <= abs(v2):
                    D[(i,k)] = [(p, v1)]
                else:
                    D[(i,k)] = [(p, v2)]
    return D

def get_monomial(R, a):
    result = R("1")
    for x,p in zip(R.gens(), a):
        result *= x**p
    return result

def dict2map(D, R):
    F = [R("0") for x in R.gens()]
    for i,k in D:
        F[i] += R(str(D[(i,k)]))*get_monomial(R,k)
    return F

def dicts_union(A, B):
    result = {k: [] for k in A.keys() | B.keys()}
    for k in A:
        result[k] += A[k]
    for k in B:
        result[k] += B[k]
    return result

def crt(D):
    result = {}
    for k in D:
        m = [t[0] for t in D[k]]
        n = [t[1] for t in D[k]]
        N = reduce(lambda x,y:x*y, m)
        temp = CRT(n,m)
        t1 = N - temp
        if abs(t1) < abs(temp):
            temp = -t1
        result[k] = temp
    return result
