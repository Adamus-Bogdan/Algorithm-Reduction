"""
This file contains program which inverts the mapping using our improved approach
"""
import sys
from mappings import mappings, names
from algorithms import algorithms
from operator import itemgetter

if __name__ == '__main__':
    debug = len(sys.argv) > 1 and sys.argv[1] == "True"
    for n in names:
        mapping = mappings[n]
        res = []
        for alg in algorithms:
            algorithm = algorithms[alg]
            res.append(tuple((alg, algorithm(mapping, debug))))

        s = sorted(res, key=itemgetter(1))
        print("============ " + n + " ============")
        for a, t in s:
            print("{0} => {1}".format(a, t))

