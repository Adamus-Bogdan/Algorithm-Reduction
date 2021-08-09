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
import textwrap
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from mappings import mappings
from algorithms import algorithms, maple_methods

if __name__ == '__main__':

    parser = ArgumentParser(
            prog="sage main.py",
            formatter_class=RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('''
            This is application to inverse polynomial mappings using various algorithms.

            For details see file README.md.
            

            '''))
    parser.add_argument(
            "-d", "--debug", 
            action="store_true",
            help="Turn on debug", 
            default=False
    )
    parser.add_argument(
            "-v", "--verify", 
            action="store_true",
            help="Turn on verifying if result is inversion", 
            default=False
    )
    parser.add_argument(
            "-j", "--jacobian",
            action="store_true",
            help="Turn on checking if jacobian is constant",
            default=False
    )
    parser.add_argument(
            "-e", "--method",
            metavar="METHOD",
            nargs=1,
            type=str,
            help="Choose Groebner basis mathod for maple, default value is ''",
            choices=maple_methods,
            default='',
            required=False
    )

    required = parser.add_argument_group('required named arguments')
    required.add_argument(
            "-a", "--algorithm", 
            metavar="ALG", 
            nargs=1, 
            type=str, 
            help="Choose algorithm to run",
            choices=list(algorithms.keys()),
            required=True
    )
    required.add_argument(
            "-m", "--mapping", 
            metavar="MAPPING",
            nargs=1, 
            type=str, 
            help="Choose mapping to study",
            choices=list(mappings.keys()),
            required=True
    )
    args = parser.parse_args()

    if not args.algorithm or not args.mapping:
        parser.print_help()
    else:
        algorithm = algorithms[args.algorithm[0]]
        mapping = mappings[args.mapping[0]]

        if args.jacobian:
            mapping.check_jacobian()

        if len(args.method) > 0:
            duration = algorithm(mapping, args.debug, args.verify, args.method[0])
        else:
            duration = algorithm(mapping, args.debug, args.verify, "")
        if args.method == "":
            print(f"Inversing map '{args.mapping[0]}' using algorithm '{args.algorithm[0]}' took {duration} s")
        else:
            print(f"Inversing map '{args.mapping[0]}' using algorithm '{args.algorithm[0]}' (method='{args.method}') took {duration} s")

