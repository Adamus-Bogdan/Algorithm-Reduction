"""
This file contains definitions of algorithms available in our program
"""
from sage.all import *

from time import time
import algorithm_abch
import algorithm_gb
from crt import map2dict, dict2map, dicts_union, fill_gaps, my_crt


def algo_abch(mapping, debug, verify, method):
    """
    This function inverses input mapping using ordinary ABCH algorithm.
    For more details see README.md file
    :param mapping: mapping to inverse
    :param debug: flag if function should print additional output
    :return: execution time
    """
    begin = time()
    G = algorithm_abch.algorithm(mapping, debug, method)
    end = time()
    #if debug:
    #    print(str(G))
    if verify:
        mapping.check_inversion(G)
    return end-begin


def _algo_gb(mapping, debug, verify, engine, method):
    """
    This function inverses input mapping using algorithm based on Groebner basis.
    For more details see README.md file
    :param mapping: mapping to inverse
    :param debug: flag if function should print additional output
    :return: execution time
    """
    begin = time()
    G = algorithm_gb.algorithm(mapping, debug, engine, method)
    end = time()
    #if debug:
    #    print(str(G))
    if verify:
        mapping.check_inversion(G)
    return end-begin


def _algo_ff(mapping, debug, verify, inversion_alg, method):
    """
    This function inverses input mapping using ordinary improved ABCH algorithm which uses Chinese Remainder Theorem
    For more details see README.md file
    :param mapping: mapping to inverse
    :param debug: flag if function should print additional output
    :return: execution time
    """
    BEGIN = time()
    # Step 1: clear denominators in input mapping 
    segre_mapping = mapping.segre_homotopy()

    if mapping.r == 1:
        destination_mapping = mapping
    else:
        destination_mapping = segre_mapping

    C = {}
    # Step 2: for every prime number p
    for p in segre_mapping.primes:
        # Step 2.1: reduce mapping F modulo p
        mapping_p = segre_mapping.reduce_mapping(p)
        # Step 2.2: perform base algorithm for reduced mapping
#         Gp = algorithm_abch.algorithm(mapping_p, debug, parallel)
        Gp = inversion_alg(mapping_p, debug)
        # Step 2.3: transform inversion of reduced mapping into dictionary
        Dp = map2dict(Gp.F, segre_mapping.imaginary, p)
        # Step 2.4: remember the coefficients in this mapping
        C = dicts_union(C, Dp)

    # Step 3: Use Chinese Reminder Theory to obtain candidate for global inverse
    C = fill_gaps(C, mapping.primes)
    D = my_crt(C, mapping.R)
    G = dict2map(D, destination_mapping)
    END = time()
    
    #if debug:
    #    print(str(G))

    # Step 4: Check if candidate is really inverse
    if verify:
        destination_mapping.check_inversion(G)
    return END - BEGIN


def algo_abch_crt_parallel(mapping, debug, verify, method):
    return _algo_ff(mapping, debug, verify, lambda f, d: algorithm_abch.algorithm(f, d, True, method), method)


def algo_abch_crt(mapping, debug, verify, method):
    return _algo_ff(mapping, debug, verify, lambda f, d: algorithm_abch.algorithm(f, d, False, method), method)


def algo_gb_sage(mapping, debug, verify, method):
    return _algo_gb(mapping, debug, verify, "sage", method)


def algo_gb_sage_crt(mapping, debug, verify, method):
    return _algo_ff(mapping, debug, verify, lambda f,d : algorithm_gb.algorithm(f, d, "sage", method), method)


def algo_gb_maple(mapping, debug, verify, method):
    return _algo_gb(mapping, debug, verify, "maple", method)


def algo_gb_maple_crt(mapping, debug, verify, method):
    return _algo_ff(mapping, debug, verify, lambda f,d : algorithm_gb.algorithm(f, d, "maple", method), method)


maple_methods = ["", "fgb", "maplef4", "buchberger", "fglm", "walk", "direct", "convert"]


algorithms = {
    "GB_SAGE": algo_gb_sage, 
    "GB_SAGE_CRT": algo_gb_sage_crt, 
    "ABCH": algo_abch, 
    "ABCH_CRT": algo_abch_crt, 
    "ABCH_CRT_PARALLEL": algo_abch_crt_parallel
}

methods = {
    "GB_SAGE": [""], 
    "GB_SAGE_CRT": [""], 
    "ABCH": [""], 
    "ABCH_CRT": [""], 
    "ABCH_CRT_PARALLEL": [""]
}


try:
    if "Basis" in str(maple("with(Groebner)")):
        algorithms["GB_MAPLE"] = algo_gb_maple
        algorithms["GB_MAPLE_CRT"] = algo_gb_maple_crt
        methods["GB_MAPLE"] = maple_methods
        methods["GB_MAPLE_CRT"] =  maple_methods
except:
    pass
    
