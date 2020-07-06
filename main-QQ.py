"""
This file contains full program which inverts the mapping using our base approach
"""
import sys
from time import time
from algorithm_abch import algorithm
from utils import check_inversion


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'F':
            from mapping_F import F, R
        elif sys.argv[1] == 'W':
            from mapping_W import F, R
        else:
            raise Exception("You need to provide which mapping you want to inverse")
    else:
        raise Exception("You need to provide which mapping you want to inverse")

    begin = time()
    G = algorithm(F, R, False)
    end = time()

    check_inversion(F,G,R)

    print("Time necessary to inverse mapping: {0}".format(end - begin))
