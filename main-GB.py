"""
This file contains full program which inverts the mapping using 
Groebner basis method
"""
import sys
from time import time
from algorithm_gb import algorithm
from utils import check_inversion

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '1':
            from mapping_1 import F, R
        elif sys.argv[1] == '2':
            from mapping_2 import F, R
        else:
            # by default
            from mapping_1 import F, R
    else:
        # by default
        from mapping_1 import F, R
    begin = time()
    G = algorithm(F, R, False)
    end = time()

    check_inversion(F,G,R)

    print("Time necessary to inverse mapping: {0}".format(end - begin))