# Algorithm for studying polynomial maps and reductions modulo prime number

In [[1]]() we described an algorithm for inverting polynomial mappings. In [[3]]() complexity of this algorithm was estimated and moreover some aspects of the algorithm's implementation were discussed. Implementation of this algorithm can be found in this repository, in file [`algorithm_abch.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/algorithm_abch.py). This implementation works for both _Pascal finite_ and _not Pascal finite_ polynomial automorphism. Definition of _Pascal finite_ automorphisms can be found in [[2]]().

In _Algorithm for studying polynomial maps and reductions modulo prime number_ we explore properties of the algorithm, and the class of Pascal finite maps while using Segre homotopy and reductions modulo prime number.  Additionally, in this repository we present our code which illustrates improvements made in the proposed algorithm.

We use fact that calculations performed over finite fields can be more effective (they are faster and use less memory) than those performed over fields of characteristic zero. We proceed as follows.
1. perform reduction modulo some set of prime numbers
2. inverse the reduced mappings using algorithm described in [[1]]()
3. retrieve global inverse using Chinese Reminder Theorem.

One can compare the base method with our improved algorithm. Just clone this repository, you need [SageMath](http://www.sagemath.org/) software. We use the SageMath v9.3 built from sources in WSL Ubuntu (Windows Subsystem for Linux). We also used Maple 2021. We additionally installed the following library:
- `memory-profiler`
To do that, one need to execute the following command:
```bash
> sage -pip install memory_profiler
```
The main file in our project is file [`main.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/main.py). You need that file to repeat our calculations. This is python program. One can use it in following way:
```commandline
usage: sage main.py [-h] [-d] [-v] [-j] [-e METHOD] [-o FILE] [-t SECONDS] [-r MB] -a ALG -m MAPPING

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Turn on debug
  -v, --verify          Turn on verifying if result is inversion
  -j, --jacobian        Turn on checking if jacobian is constant
  -e METHOD, --method METHOD
                        Choose Groebner basis mathod for maple, default value is ''
  -o FILE, --output FILE
                        Log file
  -t SECONDS, --timeout SECONDS
                        Timeout - how long algorithm works before it will be interrupted, default value is None - it means no limit
  -r MB, --memory MB    Memory limit - how much memory can be utilized by calculations

required named arguments:
  -a ALG, --algorithm ALG
                        Choose algorithm to run
  -m MAPPING, --mapping MAPPING
                        Choose mapping to study

This is application to inverse polynomial mappings using various algorithms.

For details see file README.md.
```

One can use one of the following algorithms:
- `ABCH` - runs just ABCH algorithm with cutting improvement 
- `ABCH_CRT` - runs ABCH algorithm with cutting improvement on reduced mappings
- `GB_SAGE` - runs Groebner basis based algorithm (using Sage implementation)
- `GB_SAGE_CRT` - runs Groebner basis based algorithm (using Sage implementation) on reduced mappings
- `GB_MAPLE` - runs Groebner basis based algorithm (using Maple implementation)
- `GB_MAPLE_CRT` - runs Groebner basis based algorithm (using Maple implementation) on reduced mappings

For algorithms using Maple one can also specify method (Maple has several algorithms implemented):
- `fgb`
- `maplef4`
- `buchberger`
- `fglm`  
- `walk`
- `direct`
- `convert` 
- `default`

For algorithm ABCH one can specify method:
- `partial` - performs one substitution for each monomial separately (by default algorithm performs ona substitution for the whole polynomial)

Description of each algorithm can be found in [Maple webpage](https://www.maplesoft.com/support/help/Maple/view.aspx?path=Groebner%2FBasis_algorithms).

One can run the algorithms for following maps:
- Maps defined by Hubbers in [[5]]():
  - `H1`, `H2`, `H3`, `H4`, `H5`, `H6`, `H7`, `H8`
- Maps defined by de Bondt in [[6]]():
  - `B1`, `B2`, `B3`, `B4`, `B5`, `B6`
- Maps we use as examples in our paper:
  - `EX17`, `EX19`, `EX20`

## Notation

In this file we assume that `n`-variable polynomial mapping is a list of `n` `n`-variable polynomials:
```
F = (F_1, F_2, ..., F_n)
```
Every such a polynomial is a sum of terms. Every term is product of monomial and coefficient. The every polynomial `F_i` is in the following form:
```
F_i = X_i + H_i
```
Where `H_i` is a zero polynomial or `n`-variable polynomial of lower degree (e.g. vanishing order) at least 2.
We introduce the following notation:
- `d_i` - lower degree of polynomial `H_i`
- `D_i` - degree of polynomial `H_i`
- `D = max D_i`
- `d = min d_i`

The algorithm obtains polynomial mapping
```
G = (G_1, ... G_n)
```
which is list of `n` `n`-variable polynomials.

# Comparison between an original algorithm ABCH and its improved version (using CRT)


Let us compare execution time for ABCH and CRT-ABCH algorithms executed to inverse mapping `EX17`:
```bash
> sage main.py -a ABCH -m EX17 -v -j -t 3600 -r 20480
{'algorithm': 'ABCH', 'mapping': 'EX17', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 2887.33203125, 'duration': 1012.4808, 'status': 'OK', 'inversion_check_max_memory': -1, 'inverse_check_duration': 0.0281, 'inverse_check_status': 'OK'}
> sage main.py -a ABCH_CRT -m EX17 -v -j -t 3600 -r 20480
{'algorithm': 'ABCH_CRT', 'mapping': 'EX17', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 1720.22265625, 'duration': 235.4749, 'status': 'OK', 'inversion_check_max_memory': -1, 'inverse_check_duration': 0.0369, 'inverse_check_status': 'OK'}
```
From above output one can choose the most important data:

|Algorithm|Maximal memory utilization [MB] | Duration [s] |
|:-------:|:------------------------------:|:------------:|
|ABCH|2887.3|1012.5|
|ABCH + reduction + CRT|1720.2|235.5|

One can conclude that version with reduction and using Chinese Reminder Theorem is faster and needs much less memory to execute.

# Comparison to Groebner basis based algorithm

We compare our improved algorithm (e.g. containing reductions modulo prime numbers) to algorithm based on Groebner basis described in [[4]]().
Implementation of that algorithm can be found in [`algorithm_gb.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/algorithm_gb.py).
One can run this algorithm using script [`main.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/main.py) (as described above).

We compare time of calculating inverse mapping for two mappings using our improved approach and standard Groebner basis method.

Let us compare execution time for all algorithms executed to inverse mappings `EX19`:

```bash
> sage main.py -a ABCH -m EX19 -v -j -t 3600 -r 20480
{'algorithm': 'ABCH', 'mapping': 'EX19', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 146.95703125, 'duration': 2.0812, 'status': 'OK', 'inversion_check_max_memory': 147.921875, 'inverse_check_duration': 0.4018, 'inverse_check_status': 'OK'}
> sage main.py -a ABCH_CRT -m EX19 -v -j -t 3600 -r 20480
{'algorithm': 'ABCH_CRT', 'mapping': 'EX19', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 306.96484375, 'duration': 24.2033, 'status': 'OK', 'inversion_check_max_memory': -1, 'inverse_check_duration': 0.2676, 'inverse_check_status': 'OK'}
> sage main.py -a GB_SAGE -m EX17 -v -j -t 3600 -r 20480
{'algorithm': 'GB_SAGE', 'mapping': 'EX19', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 1507.5078125, 'status': 'TLE', 'duration': 3600}
> sage main.py -a GB_MAPLE -m EX19 -v -j -t 3600 -r 20480
{'algorithm': 'GB_MAPLE', 'mapping': 'EX19', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 14782.47265625, 'status': 'TLE', 'duration': 3600}
> sage main.py -a GB_MAPLE -m EX19 -v -j -t 3600 -r 20480 -e fgb
{'algorithm': 'GB_MAPLE', 'mapping': 'EX19', 'method': 'fgb', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 145.48828125}
> sage main.py -a GB_MAPLE -m EX19 -v -j -t 3600 -r 20480 -e maplef4
{'algorithm': 'GB_MAPLE', 'mapping': 'EX19', 'method': 'maplef4', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 11620.58203125, 'status': 'TLE', 'duration': 3600}
> sage main.py -a GB_MAPLE -m EX19 -v -j -t 3600 -r 20480 -e buchberger
{'algorithm': 'GB_MAPLE', 'mapping': 'EX19', 'method': 'buchberger', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 489.796875, 'status': 'TLE', 'duration': 3600}
> sage main.py -a GB_MAPLE -m EX19 -v -j -t 3600 -r 20480 -e fglm
{'algorithm': 'GB_MAPLE', 'mapping': 'EX19', 'method': 'fglm', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 15316.2265625, 'status': 'TLE', 'duration': 3600}
> sage main.py -a GB_MAPLE -m EX19 -v -j -t 3600 -r 20480 -e walk
{'algorithm': 'GB_MAPLE', 'mapping': 'EX19', 'method': 'walk', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 15319.296875, 'status': 'TLE', 'duration': 3600}
> sage main.py -a GB_MAPLE -m EX19 -v -j -t 3600 -r 20480 -e direct
{'algorithm': 'GB_MAPLE', 'mapping': 'EX19', 'method': 'direct', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 12021.25, 'status': 'TLE', 'duration': 3600}
> sage main.py -a GB_MAPLE -m EX19 -v -j -t 3600 -r 20480 -e convert
{'algorithm': 'GB_MAPLE', 'mapping': 'EX19', 'method': 'convert', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 15326.76171875, 'status': 'TLE', 'duration': 3600}
```

Let us collect the most interesting data in below table:

|Algorithm|Environment|Method|Maximal memory utilization [MB] | Duration [s] |
|:-------:|:---------:|:----:|:------------------------------:|:------------:|
|ABCH|SageMath|-|147.0|2.1|
|ABCH + reduction + CRT|SageMath|-|307.0|24.2|
|Groebner Basis|SageMath|-|1507.5|TLE|
|Groebner Basis|Maple|Default|14782.5|TLE|
|Groebner Basis|Maple|fgb|ERROR|ERROR|
|Groebner Basis|Maple|maplef4|11620.6|TLE|
|Groebner Basis|Maple|buchberger|489.8|TLE|
|Groebner Basis|Maple|fglm|15316.2|TLE|
|Groebner Basis|Maple|walk|15319.3|TLE|
|Groebner Basis|Maple|direct|12021.3|TLE|
|Groebner Basis|Maple|convert|15326.8|TLE|

One can see that Maple didn't manage to inverse mapping `EX19` during an hour - we set such a timeout for computations. ABCH algorithm (with cutting) needs only 2 seconds. Reductions modulo primes and using Chinese Reminder Theorem needs more time. However, it is much better than any implementation of Groebner Basis algorithm we tested.

We performed the same procedure for the mapping `EX20`:
```bash
> sage main.py -a ABCH -m EX20 -v -j -t 3600 -r 20480
2021-09-14 22:56:49 {'algorithm': 'ABCH', 'mapping': 'EX20', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 4437.390625, 'duration': 937.0894, 'status': 'OK', 'inversion_check_max_memory': 505.734375, 'inverse_check_duration': 60.8725, 'inverse_check_status': 'OK'}
> sage main.py -a ABCH_CRT -m EX20 -v -j -t 3600 -r 20480
2021-09-14 23:09:24 {'algorithm': 'ABCH_CRT', 'mapping': 'EX20', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 5486.67578125, 'duration': 688.9472, 'status': 'OK', 'inversion_check_max_memory': 505.859375, 'inverse_check_duration': 63.6832, 'inverse_check_status': 'OK'}
> sage main.py -a GB_SAGE -m EX20 -v -j -t 3600 -r 20480
2021-09-15 01:09:32 {'algorithm': 'GB_SAGE', 'mapping': 'EX20', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 2256.63671875, 'status': 'TLE', 'duration': 3600}
> sage main.py -a GB_MAPLE -m EX20 -v -j -t 3600 -r 20480
2021-09-15 15:13:00 {'algorithm': 'GB_MAPLE', 'mapping': 'EX20', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 460.984375, 'status': 'TLE', 'duration': 3600}
> sage main.py -a GB_MAPLE -m EX20 -v -j -t 3600 -r 20480 -e fgb
2021-09-15 15:13:04 {'algorithm': 'GB_MAPLE', 'mapping': 'EX20', 'method': 'fgb', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': -1}
> sage main.py -a GB_MAPLE -m EX20 -v -j -t 3600 -r 20480 -e maplef4
2021-09-15 15:14:09 {'algorithm': 'GB_MAPLE', 'mapping': 'EX20', 'method': 'maplef4', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 149.5078125, 'duration': 1.8957, 'status': 'OK', 'inversion_check_max_memory': 502.9921875, 'inverse_check_duration': 61.7232, 'inverse_check_status': 'OK'}
> sage main.py -a GB_MAPLE -m EX20 -v -j -t 3600 -r 20480 -e buchberger
2021-09-15 16:14:12 {'algorithm': 'GB_MAPLE', 'mapping': 'EX20', 'method': 'buchberger', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 12289.078125, 'status': 'TLE', 'duration': 3600}
> sage main.py -a GB_MAPLE -m EX20 -v -j -t 3600 -r 20480 -e fglm
2021-09-15 16:14:24 {'algorithm': 'GB_MAPLE', 'mapping': 'EX20', 'method': 'fglm', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 149.984375}
> sage main.py -a GB_MAPLE -m EX20 -v -j -t 3600 -r 20480 -e walk
2021-09-15 17:14:27 {'algorithm': 'GB_MAPLE', 'mapping': 'EX20', 'method': 'walk', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 430.140625, 'status': 'TLE', 'duration': 3600}
> sage main.py -a GB_MAPLE -m EX20 -v -j -t 3600 -r 20480 -e direct
2021-09-15 17:15:35 {'algorithm': 'GB_MAPLE', 'mapping': 'EX20', 'method': 'direct', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 151.421875, 'duration': 1.7515, 'status': 'OK', 'inversion_check_max_memory': 504.93359375, 'inverse_check_duration': 63.9796, 'inverse_check_status': 'OK'}
> sage main.py -a GB_MAPLE -m EX20 -v -j -t 3600 -r 20480 -e convert
2021-09-15 18:15:37 {'algorithm': 'GB_MAPLE', 'mapping': 'EX20', 'method': 'convert', 'timeout': 3600, 'memory_limit': 20480, 'jacobian_check': 'OK', 'max_memory': 485.48828125, 'status': 'TLE', 'duration': 3600}
```

We collected the most interesting data in the table below.

|Algorithm|Environment|Method|Maximal memory utilization [MB] | Duration [s] |
|:-------:|:---------:|:----:|:------------------------------:|:------------:|
|ABCH|SageMath|-|4437.4|937.1|
|ABCH + reduction + CRT|SageMath|-|5486.7|689.0|
|Groebner Basis|SageMath|-|2256.6|TLE|
|Groebner Basis|Maple|Default|461.0|TLE|
|Groebner Basis|Maple|fgb|ERROR|ERROR|
|Groebner Basis|Maple|maplef4|149.5|1.9|
|Groebner Basis|Maple|buchberger|12289.1|TLE|
|Groebner Basis|Maple|fglm|ERROR|ERROR|
|Groebner Basis|Maple|walk|430.0|TLE|
|Groebner Basis|Maple|direct|151.4|TLE|
|Groebner Basis|Maple|convert|485.5|TLE|

We run all computations with timeout equal to one hour. After this time, program stopped the algorithm execution and set the status to `TLE` (_Time Limit Exceeded_). One can notice that Maple implementation of algorithm f4 gives the results in less than 2 seconds. However, algorithm ABCH is better than any other Groebner Basis implementation we tested. This example presents that using strategy of reducing mapping modulo primes gives time execution improvement.

One can check these results herself (or himself). One can also check our paper _Algorithm for studying polynomial maps and reductions modulo prime number_.


# Hardware details

All examples were executed on Windows 10 machine with 16 GB RAM and intel i7 processor. SageMath 9.3 and Maple 2021 software was installed in WSL (Windows Subsystem for Linux).


# Future work

In our opinion this is worth to:
- study parallel computations of ABCH algorithm - there are several strategies to use parallel computations in ABCH algorithm implementation. Some ideas can be found in Pawel' PhD thesis [[7]](). In case of difficulties in finding this thesis, please reach him directly ([pawel.bogdan1@gmail.com](mailto:pawel.bogdan1@gmail.com)).
- check out other implementation of Groebner Basis algorithms - there is very promising paper [[8]]() with effective approach to F5 algorithm. We tried to reach the authors to compare implementations. They haven't replied yet. There is also Giac software which also has effective implementation of looking for Groebner basis.
- run some benchmark tests for known set of polynomial systems. E. g. [this page](http://www.cecm.sfu.ca/%7Erpearcea/mgb.html) or [that one](http://magma.maths.usyd.edu.au/~allan/gb/)


# Bibliography

1. E. Adamus, P. Bogdan, T. Crespo and Z. Hajto, _An effective study of polynomial maps_, Journal of Algebra and Its Applications, Vol. 16, No. 08, 1750141 (2017)
2. E. Adamus, P. Bogdan, T. Crespo and Z. Hajto, _Pascal finite polynomial automorphisms_, Journal of Algebra and Its Applications, Vol. 18, No. 07, 1950124 (2019)
3. P. Bogdan, _Complexity of the inversion algorithm of polynomial mappings_, Schedae Informaticae, 2016, Volume 25, pages 209–225
4. A. van den Essen, _Polynomial Automorphisms and the Jacobian Conjecture_, Progress in Mathematics, 2000th Edition
5. E.-M. Hubbers, _The Jacobian Conjecture: Cubic homogeneous maps in dimension four_.  Master’s thesis, University of Nijmegen. [URL](http://www.cs.ru.nl/~hubbers/pubs/ivascriptie.pdf). Directed by A. van den Essen.
6. M. Bondt,  _Homogeneous keller maps_. Physical Review Letters, 01 2009.
7. P. Bogdan, _Computational study of polynomial automorphisms_, PhD thesis, Jagiellonian University.
8. M. Bardet, J.-Ch. Faugère, B. Salvy, _On the complexity of the F5 Gröbner basis algorithm_, Journal of Symbolic Computation, Vol. 70, 49-70 (2015)