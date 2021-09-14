"""
This file contains definitions of algorithms available in our program
"""
from sage.all import *
import sys
from time import time
from multiprocessing import Process, Manager
import psutil
from memory_profiler import memory_usage
import algorithm_abch
import algorithm_gb
from crt import map2dict, dict2map, dicts_union, fill_gaps, my_crt


DURATION_DIGITS = 4


def _algo_abch(*, mapping, debug, results, method=None, **kwargs):
    """
    This function inverses input mapping using ordinary ABCH algorithm.
    For more details see README.md file
    """
    start = time()
    g = algorithm_abch.algorithm(mapping=mapping, debug=debug, method=method)
    finish = time()
    results['duration'] = round(finish-start, DURATION_DIGITS)
    results['G'] = g
    results['F'] = mapping


def _algo_gb(*, mapping, debug, engine, method, results, **kwargs):
    """
    This function inverses input mapping using algorithm based on Groebner basis.
    For more details see README.md file
    """
    start = time()
    g = algorithm_gb.algorithm(mapping=mapping, debug=debug, engine=engine, method=method)
    finish = time()
    results['duration'] = round(finish-start, DURATION_DIGITS)
    results['G'] = g
    results['F'] = mapping


def _algo_ff(*, mapping, debug, inversion_algorithm, results, **kwargs):
    """
    This function inverses input mapping using ordinary improved ABCH algorithm which uses Chinese Remainder Theorem
    For more details see README.md file
    """
    start_of_all = time()
    # Step 1: clear denominators in input mapping
    segre_mapping = mapping.segre_homotopy()

    if mapping.r == 1:
        destination_mapping = mapping
    else:
        destination_mapping = segre_mapping

    map_of_coefficients = {}
    # Step 2: for every prime number p
    for p in segre_mapping.primes:
        # Step 2.1: reduce mapping F modulo p
        mapping_p = segre_mapping.reduce_mapping(p)
        # Step 2.2: perform base algorithm for reduced mapping
        #         Gp = algorithm_abch.algorithm(mapping_p, debug, parallel)
        g_p = inversion_algorithm(mapping_p, debug)
        # Step 2.3: transform inversion of reduced mapping into dictionary
        d_p = map2dict(g_p.F, segre_mapping.imaginary, p)
        # Step 2.4: remember the coefficients in this mapping
        map_of_coefficients = dicts_union(map_of_coefficients, d_p)
    # Step 3: Use Chinese Reminder Theory to obtain candidate for global inverse
    map_of_coefficients = fill_gaps(map_of_coefficients, mapping.primes)
    resulting_map = my_crt(map_of_coefficients)
    g = dict2map(resulting_map, destination_mapping)
    finish_of_all = time()
    results['duration'] = round(finish_of_all-start_of_all, DURATION_DIGITS)
    results['F'] = destination_mapping
    results['G'] = g


# https://stackoverflow.com/questions/6549669/how-to-kill-process-and-child-processes-from-python
def kill_process(process):
    parent_process = psutil.Process(process.pid)
    for child in parent_process.children(recursive=True):
        child.kill()
    parent_process.kill()


def monitor_memory_usage(*, process, memory_limit, results, timeout=1, i_val=1, prefix=''):
    if memory_limit is None:
        return
    results[f'{prefix}max_memory'] = -1
    start = time()
    while True:
        mem = memory_usage(
                process.pid,
                interval=i_val,
                timestamps=True,
                timeout=timeout,
                multiprocess=True,
                include_children=True,
                max_usage=True)
        if mem > results[f'{prefix}max_memory']:
            results[f'{prefix}max_memory'] = mem
        if mem > memory_limit:
            finish = time()
            kill_process(process)
            results[f'{prefix}status'] = 'MEM'
            results[f'{prefix}duration'] = round(finish - start, DURATION_DIGITS)
            return
        sleep(1)


def run_algorithm(*, alg, mapping, debug, verify, method, engine, inversion_algorithm, check_jacobian,
                  timeout, memory_limit, params):
    with Manager() as manager:
        try:
            d = manager.dict()

            for p in params:
                temp = params[p]
                if temp is not None and temp != "":
                    d[p] = temp

            if timeout is not None:
                d['timeout'] = timeout

            if memory_limit is not None:
                d['memory_limit'] = memory_limit

            if check_jacobian:
                if mapping.check_jacobian():
                    d['jacobian_check'] = 'OK'
                else:
                    d['jacobian_check'] = 'ERROR'
            else:
                d['jacobian_check'] = 'skipped'

            process = Process(target=alg, kwargs={
                'mapping': mapping,
                'debug': debug,
                'method': method,
                'engine': engine,
                'inversion_algorithm': inversion_algorithm,
                'results': d
            })
            monitor = Process(target=monitor_memory_usage,
                              kwargs={'process': process, 'memory_limit': memory_limit, 'results': d})
            process.start()
            monitor.start()
            process.join(timeout)
            if process.is_alive():
                kill_process(process)
                d['status'] = "TLE"
                d['duration'] = timeout

            if monitor.is_alive():
                monitor.terminate()

            if 'G' in d and 'F' in d:
                d['status'] = 'OK'

                if verify:
                    process = Process(target=run_inverse_check, kwargs={'results': d})
                    monitor = Process(target=monitor_memory_usage,
                                      kwargs={'process': process, 'memory_limit': memory_limit,
                                              'results': d, 'prefix': 'inversion_check_'})
                    process.start()
                    monitor.start()
                    process.join(timeout)
                    if process.is_alive():
                        kill_process(process)
                        d['inverse_check_status'] = 'TLE'
                        d['inverse_check_duration'] = timeout
                    if monitor.is_alive():
                        monitor.terminate()
                else:
                    d['inverse_check_status'] = 'skipped'
                del d['G']
                del d['F']
            return d.copy()
        except:
            d['status'] = 'ERROR'
            if debug:
                print("Unexpected error:", sys.exc_info()[0])


def run_inverse_check(*, results):
    f = results['F']
    g = results['G']
    start = time()
    res = f.check_inversion(g)
    finish = time()
    results['inverse_check_duration'] = round(finish-start, DURATION_DIGITS)
    if res:
        results['inverse_check_status'] = 'OK'
    else:
        results['inverse_check_status'] = 'ANS'


def algo_abch(*, mapping, debug, verify, method, check_jacobian, timeout, memory_limit, params):
    return run_algorithm(
            alg=_algo_abch,
            mapping=mapping,
            debug=debug,
            verify=verify,
            method=method,
            engine=None,
            inversion_algorithm=None,
            check_jacobian=check_jacobian,
            timeout=timeout,
            memory_limit=memory_limit,
            params=params
    )


def algo_abch_crt(*, debug, verify, check_jacobian, timeout, memory_limit, params, method, **kwargs):
    return run_algorithm(
            alg=_algo_ff,
            mapping=kwargs['mapping'],
            debug=debug,
            verify=verify,
            method=method,
            engine=None,
            inversion_algorithm=lambda f, d: algorithm_abch.algorithm(mapping=f, debug=d, method=method),
            check_jacobian=check_jacobian,
            timeout=timeout,
            memory_limit=memory_limit,
            params=params
    )


def algo_gb_sage(*, mapping, debug, verify, method, check_jacobian, timeout, memory_limit, params):
    return run_algorithm(
            alg=_algo_gb,
            mapping=mapping,
            debug=debug,
            verify=verify,
            method=method,
            engine='sage',
            inversion_algorithm=None,
            check_jacobian=check_jacobian,
            timeout=timeout,
            memory_limit=memory_limit,
            params=params
    )


def algo_gb_sage_crt(*, mapping, debug, verify, method, check_jacobian, timeout, memory_limit, params):
    return run_algorithm(
            alg=_algo_ff,
            mapping=mapping,
            debug=debug,
            verify=verify,
            method=method,
            engine=None,
            inversion_algorithm=lambda f, d: algorithm_gb.algorithm(mapping=f, debug=d, engine="sage", method=method),
            check_jacobian=check_jacobian,
            timeout=timeout,
            memory_limit=memory_limit,
            params=params
    )


def algo_gb_maple(*, mapping, debug, verify, method, check_jacobian, timeout, memory_limit, params):
    return run_algorithm(
            alg=_algo_gb,
            mapping=mapping,
            debug=debug,
            verify=verify,
            method=method,
            engine="maple",
            inversion_algorithm=None,
            check_jacobian=check_jacobian,
            timeout=timeout,
            memory_limit=memory_limit,
            params=params
    )


def algo_gb_maple_crt(*, mapping, debug, verify, method, check_jacobian, timeout, memory_limit, params):
    return run_algorithm(
            alg=_algo_ff,
            mapping=mapping,
            debug=debug,
            verify=verify,
            method=method,
            engine=None,
            inversion_algorithm=lambda f, d: algorithm_gb.algorithm(mapping=f, debug=d, engine="maple", method=method),
            check_jacobian=check_jacobian,
            timeout=timeout,
            memory_limit=memory_limit,
            params=params
    )


maple_methods = ["", "fgb", "maplef4", "buchberger", "fglm", "walk", "direct", "convert", "default"]
sage_methods = ["", "partial"]


algorithms = {
    "GB_SAGE": algo_gb_sage, 
    "GB_SAGE_CRT": algo_gb_sage_crt, 
    "ABCH": algo_abch, 
    "ABCH_CRT": algo_abch_crt, 
    "GB_MAPLE": algo_gb_maple,
    "GB_MAPLE_CRT": algo_gb_maple_crt
}

methods = {
    "GB_SAGE": [""], 
    "GB_SAGE_CRT": [""], 
    "ABCH": sage_methods,
    "ABCH_CRT": sage_methods,
    "GB_MAPLE": maple_methods,
    "GB_MAPLE_CRT": maple_methods
}
