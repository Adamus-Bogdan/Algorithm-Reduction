import sys
from sage.all import *

def get_terms(p):
    return [m*p.monomial_coefficient(m) for m in p.monomials()]

def filter_terms(p, limit):
    result = 0
    for term in get_terms(p):
        if term.degree() <= limit:
            result += term
    return result

def find_degrees(F,R):
    n = len(F)
    min_d = sys.maxsize
    max_D = -1
    lower_degrees = []
    for i in range(n):
        monomials = (F[i] - R.gens()[i]).monomials()
        if len(monomials) == 0:
            lower_degrees.append(sys.maxsize)
        else:
            temp_degrees = [m.degree() for m in monomials]
            d = min(temp_degrees)
            if d < min_d:
                min_d = d
            D = max(temp_degrees)
            if D > max_D:
                max_D = D
            lower_degrees.append(d)
    return max_D, min_d, lower_degrees

def inverse_algorithm(F, R, i, debug):
    if debug:
        print('---------------------------------------------')
        print('Executing algorithm for {0}'.format(R.gens()[i]))
    p = R.gens()[i]
    result = R.gens()[i]
    step = 1
    n = len(F)
    max_D, min_d, lower_degrees = find_degrees(F,R)
    degree_limit = max_D**(n-1)
    if min_d > 1:
        limit = floor((max_D**(n - 1) - lower_degrees[i])/(min_d - 1) + 1)+1
    else:
        limit = degree_limit
    if lower_degrees[i] == sys.maxsize:
        if debug:
            print('There is no need to perform the algorithm')
        return R.gens()[i]
    if debug:
        print('Maximum number of steps: {0}'.format(limit))
        print('Inversion degree boundary: {0}'.format(degree_limit))
    while True:
        p -= p(F)
        result += p
        if p == 0:
            if debug:
                print('P_{0} = 0'.format(step))
            return result
        else:
            degrees = [m.degree() for m in p.monomials()]
            degree = max(degrees)
            ldegree = min(degrees)
            if debug:
                print('P_{0} has degree: {1}, ldegree: {2}, length: {3}'.format(step, degree, ldegree, len(degrees)))
            if step == limit:
                if debug:
                    print('NOT PASCAL FINITE!')
                return filter_terms(result, degree_limit)
        step += 1
    
    
def algorithm(F, R, debug=True):
    if debug:
        print('==================== Mapping ====================')
        print(R)
        for i in range(len(F)):
            print('F_{0}  = {1}'.format(i+1, F[i]))
    return [inverse_algorithm(F,R,i, debug) for i in range(len(F))]

