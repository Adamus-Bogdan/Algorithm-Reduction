"""
This file contains full program which inverts the mapping using our base approach
"""
import sys
from time import time
from algorithm import algorithm
from utils import check_inversion
from mapping import F, R

if __name__ == '__main__':
    begin = time()
    G = algorithm(F, R, False)
    end = time()

    check_inversion(F,G,R)

    print("Time necessary to inverse mapping: {0}".format(end - begin))
