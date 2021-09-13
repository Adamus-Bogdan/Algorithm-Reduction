"""
This file contains main program of this repository.
"""
import textwrap
from datetime import datetime
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from mappings import mappings
from algorithms import algorithms, maple_methods, sage_methods

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
            help="Choose Groebner basis method for maple, default value is ''",
            choices=maple_methods + sage_methods,
            default='',
            required=False
    )
    parser.add_argument(
            "-o", "--output",
            metavar="FILE",
            nargs=1,
            type=str,
            help="Log file",
            default="log.out",
            required=False
    )
    parser.add_argument(
            '-t', '--timeout',
            metavar="SECONDS",
            nargs=1,
            type=int,
            help="Timeout - how long algorithm works before it will be interrupted, " +
                 "default value is None - it means no limit",
            default=None,
            required=False
    )
    parser.add_argument(
            '-r', '--memory',
            metavar="MB",
            nargs=1,
            type=int,
            help="Memory limit - how much memory can be utilized by calculations",
            default=None,
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
        with open(args.output, "a") as log_file:
            mapping = mappings[args.mapping[0]]
            begin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if len(args.method) > 0:
                meth = args.method[0]
            else:
                meth = ""
            
            if args.timeout is None or len(args.timeout) == 0:
                timeout = None
            else:
                timeout = args.timeout[0]

            if args.memory is None or len(args.memory) == 0:
                memory_limit = None
            else:
                memory_limit = args.memory[0]
            
            result = algorithm(
                    mapping=mapping, 
                    debug=args.debug, 
                    verify=args.verify, 
                    method=meth, 
                    check_jacobian=args.jacobian, 
                    timeout=timeout, 
                    memory_limit=memory_limit,
                    params={"algorithm": args.algorithm[0], "mapping": args.mapping[0], "method": meth}
            ) 
            end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            msg = end + " " + str(result)

            print(msg)
            log_file.write(msg + "\n")
