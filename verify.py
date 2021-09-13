"""
This file contains code that verifies if our program works correctly
"""
from algorithms import algorithms
from mappings import mappings

tm = ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "B1"]

mm = ["", "fgb", "maplef4", "buchberger"]
sm = ["", "at-once", "parallel"]

alg = ["GB_SAGE", "GB_SAGE_CRT", "ABCH", "ABCH_CRT", "GB_MAPLE", "GB_MAPLE_CRT"]

mh = {
    "GB_SAGE": [""],
    "GB_SAGE_CRT": [""],
    "ABCH": sm,
    "ABCH_CRT": sm,
    "GB_MAPLE": mm,
    "GB_MAPLE_CRT": [""]
}


def verify(debug=False):
    for al in alg:
        for method in mh[al]:
            for mapping in tm:
                if mappings[mapping].imaginary and method == "fgb":
                    continue
                if mapping == "B1" and al == "GB_MAPLE_CRT":
                    continue
                t = algorithms[al](
                        mapping=mappings[mapping],
                        debug=False, 
                        verify=True, 
                        method=method, 
                        check_jacobian=True, 
                        timeout=None,
                        memory_limit=None,
                        params={"algorithm": al, "mapping": mapping, "method": method})
                if debug:
                    print(f"{t}")
                assert "inverse_check_status" in t and t["inverse_check_status"] == "OK", \
                    f"ERROR for algorithm {al}({method}) for mapping {mapping}"


if __name__ == '__main__':
    verify(True)
