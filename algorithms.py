"""
This file contains definitions of algorithms available in our program
"""
from time import time
import algorithm_abch
import algorithm_gb
from crt import map2dict, dict2map, dicts_union, fill_gaps, crt


def algo_qq(mapping, debug):
    """
    This function inverses input mapping using ordinary ABCH algorithm.
    For more details see README.md file
    :param mapping: mapping to inverse
    :param debug: flag if function should print additional output
    :return: execution time
    """
    begin = time()
    G = algorithm_abch.algorithm(mapping, debug)
    end = time()
    if debug:
        print(str(G))
    return end-begin


def algo_gb(mapping, debug):
    """
    This function inverses input mapping using algorithm based on Groebner basis.
    For more details see README.md file
    :param mapping: mapping to inverse
    :param debug: flag if function should print additional output
    :return: execution time
    """
    begin = time()
    G = algorithm_gb.algorithm(mapping, debug)
    end = time()
    if debug:
        print(str(G))
    mapping.check_inversion(G)
    return end-begin


def _algo_ff(mapping, debug, parallel):
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
        Gp = algorithm_abch.algorithm(mapping_p, debug, parallel)
        # Step 2.3: transform inversion of reduced mapping into dictionary
        Dp = map2dict(Gp.F, segre_mapping.imaginary, p)
        # Step 2.4: remember the coefficients in this mapping
        C = dicts_union(C, Dp)

    # Step 3: Use Chinese Reminder Theory to obtain candidate for global inverse
    C = fill_gaps(C, mapping.primes)
    D = crt(C, mapping.R)
    G = dict2map(D, destination_mapping)
    END = time()
    
    if debug:
        print(str(G))

    # Step 4: Check if candidate is really inverse
    destination_mapping.check_inversion(G)
    return END - BEGIN


def algo_ff_parallel(mapping, debug):
    return _algo_ff(mapping, debug, True)


def algo_ff_seq(mapping, debug):
    return _algo_ff(mapping, debug, False)


algorithms = {"GB": algo_gb, "QQ": algo_qq, "FF": algo_ff_seq, "PARALLEL": algo_ff_parallel}
