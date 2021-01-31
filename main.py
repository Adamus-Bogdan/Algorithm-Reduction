"""
This file contains program which inverts the mapping using our improved approach
"""
import sys
from mappings import mappings
from algorithms import algorithms

if __name__ == '__main__':
    mapping = mappings[sys.argv[1]]
    algorithm = algorithms[sys.argv[2]]
    debug = len(sys.argv) > 3 and sys.argv[3] == "True"
    print("Time necessary to inverse mapping: {0}".format(algorithm(mapping, debug)))
