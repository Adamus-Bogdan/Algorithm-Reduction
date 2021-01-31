"""
This file contains full program which inverts the mapping using our base approach
"""
import sys
from time import time
import algorithm_abch
import algorithm_gb
from mappings import mappings
from crt import map2dict, dict2map, dicts_union, crt


def algo_qq(mapping, debug):
    begin = time()
    G = algorithm_abch.algorithm(mapping, debug)
    end = time()
    mapping.check_inversion(G)
    return end-begin


def algo_gb(mapping, debug):
    begin = time()
    G = algorithm_gb.algorithm(mapping, debug)
    end = time()
    mapping.check_inversion(G)
    return end-begin


def algo_ff(mapping, debug):
    BEGIN = time()
    # Step 1: clear denominators in input mapping 
    segre_mapping = mapping.segre_homotopy()

    C = {}
    # Step 2: for every prime number p
    for p in segre_mapping.primes:
        # Step 2.1: reduce mapping F modulo p
        mapping_p = segre_mapping.reduce_mapping(p)
        # Step 2.2: perform base algorithm for reduced maping
        Gp = algorithm_abch.algorithm(mapping_p, debug)
        # Step 2.3: transform inversion of reduced mapping into dictionary
        Dp = map2dict(Gp, p, debug)
        # Step 2.4: remember the coefficients in this mapping
        C = dicts_union(C, Dp)

    # Step 3: Use Chinese Reminder Theory to obtain candidate for global inverse
    D = crt(C)
    G = dict2map(D, segre_mapping.R)
    END = time()
    # Step 4: Check if candidate is really inverse
    segre_mapping.check_inversion(G)
    return END - BEGIN



algorithms = {"GB": algo_gb, "QQ": algo_qq, "FF": algo_ff}


