"""
This file contains program which inverts the mapping using our improved approach
"""
import sys
from mappings import mappings
from algorithms import algorithms
from operator import itemgetter

if __name__ == '__main__':
    mapping = mappings[sys.argv[1]]
    debug = len(sys.argv) > 2 and sys.argv[2] == "True"
    res = []
    for alg in algorithms:
        algorithm = algorithms[alg]
        res.append(tuple((alg, algorithm(mapping, debug))))

    s = sorted(res, key=itemgetter(1))
    for a, t in s:
        print("{0} => {1}".format(a, t))

