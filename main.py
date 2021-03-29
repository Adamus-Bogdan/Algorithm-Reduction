"""
This file contains main program of this repository.
The program gets the following arguments:
- name of mapping to inverse - possible mappings are listed in mappings.py file
- name of algorithm used to inverse - possible algorithms are listed in algorithms.py file
  you can check README.md file as well
- optional True if you want to have additional output, if not provided or different value provided
  program will print only duration time of inverting
"""
import sys
from mappings import mappings
from algorithms import algorithms

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You need to provide mapping's name as first argument of this program")
        print("You have the following possibilities:")
        for m in mappings:
            print(f" - {m}")
        print("Their definitions can be found in mappings.py file")
        sys.exit(0)

    mapping = mappings[sys.argv[1]]
    mapping.check_jacobian()

    if len(sys.argv) < 3:
        print("You need to provide algorithm's name as second argument of this program")
        print("You have the following possibilities:")
        for a in algorithms:
            print(f" - {a}")
        print("For details check README.md file")
        sys.exit(0)

    algorithm = algorithms[sys.argv[2]]
    debug = len(sys.argv) > 3 and sys.argv[3] == "True"

    print("Time necessary to inverse mapping: {0}".format(algorithm(mapping, debug)))
