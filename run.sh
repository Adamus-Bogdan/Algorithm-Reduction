#!/bin/bash

sage main.py -a ABCH -m EX17 -v -j -t 3600 -r 20480
sage main.py -a ABCH_CRT -m EX17 -v -j -t 3600 -r 20480

sage main.py -a ABCH -m EX19 -v -j -t 3600 -r 20480
sage main.py -a ABCH_CRT -m EX19 -v -j -t 3600 -r 20480

sage main.py -a ABCH -m EX20 -v -j -t 3600 -r 20480
sage main.py -a ABCH_CRT -m EX20 -v -j -t 3600 -r 20480

sage main.py -a GB_SAGE -m EX17 -v -j -t 3600 -r 20480
sage main.py -a GB_SAGE_CRT -m EX17 -v -j -t 3600 -r 20480

sage main.py -a GB_SAGE -m EX19 -v -j -t 3600 -r 20480
sage main.py -a GB_SAGE_CRT -m EX19 -v -j -t 3600 -r 20480

sage main.py -a GB_SAGE -m EX20 -v -j -t 3600 -r 20480
sage main.py -a GB_SAGE_CRT -m EX20 -v -j -t 3600 -r 20480

sage main.py -a GB_maple -m EX17 -v -j -t 3600 -r 20480
sage main.py -a GB_maple -m EX17 -v -j -t 3600 -r 20480 -e fgb
sage main.py -a GB_maple -m EX17 -v -j -t 3600 -r 20480 -e maplef4
sage main.py -a GB_maple -m EX17 -v -j -t 3600 -r 20480 -e buchberger
sage main.py -a GB_maple -m EX17 -v -j -t 3600 -r 20480 -e fglm
sage main.py -a GB_maple -m EX17 -v -j -t 3600 -r 20480 -e walk
sage main.py -a GB_maple -m EX17 -v -j -t 3600 -r 20480 -e direct
sage main.py -a GB_maple -m EX17 -v -j -t 3600 -r 20480 -e convert

sage main.py -a GB_maple -m EX19 -v -j -t 3600 -r 20480
sage main.py -a GB_maple -m EX19 -v -j -t 3600 -r 20480 -e fgb
sage main.py -a GB_maple -m EX19 -v -j -t 3600 -r 20480 -e maplef4
sage main.py -a GB_maple -m EX19 -v -j -t 3600 -r 20480 -e buchberger
sage main.py -a GB_maple -m EX19 -v -j -t 3600 -r 20480 -e fglm
sage main.py -a GB_maple -m EX19 -v -j -t 3600 -r 20480 -e walk
sage main.py -a GB_maple -m EX19 -v -j -t 3600 -r 20480 -e direct
sage main.py -a GB_maple -m EX19 -v -j -t 3600 -r 20480 -e convert

sage main.py -a GB_maple -m EX20 -v -j -t 3600 -r 20480
sage main.py -a GB_maple -m EX20 -v -j -t 3600 -r 20480 -e fgb
sage main.py -a GB_maple -m EX20 -v -j -t 3600 -r 20480 -e maplef4
sage main.py -a GB_maple -m EX20 -v -j -t 3600 -r 20480 -e buchberger
sage main.py -a GB_maple -m EX20 -v -j -t 3600 -r 20480 -e fglm
sage main.py -a GB_maple -m EX20 -v -j -t 3600 -r 20480 -e walk
sage main.py -a GB_maple -m EX20 -v -j -t 3600 -r 20480 -e direct
sage main.py -a GB_maple -m EX20 -v -j -t 3600 -r 20480 -e convert
