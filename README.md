# Algorithm for studying polynomial maps and reductions modulo prime number

In [[1]]() we described an algorithm for inverting polynomial mappings. In [[3]]() complexity of this algorithm was estimated and moreover some aspects of the algorithm's implementation were discussed. Implementation of this algorithm can be found in this repository, in file [`algorithm_abch.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/algorithm_abch.py). This implementation works for both _Pascal finite_ and _not Pascal finite_ polynomial automorphism. Definition of _Pascal finite_ automorphisms can be found in [[2]]().

In _Algorithm for studying polynomial maps and reductions modulo prime number_ we explore properties of the algorithm, and the class of Pascal finite maps while using Segre homotopy and reductions modulo prime number.  Additionally, in this repository we present our code which illustrates improvements made in the proposed algorithm.

We use fact that calculations performed over finite fields can be more effective (they are faster and use less memory) than those performed over fields of characteristic zero. We proceed as follows.
1. perform reduction modulo some set of prime numbers
2. inverse the reduced mappings using algorithm described in [[1]]()
3. retrieve global inverse using Chinese Reminder Theorem.

One can compare the base method with our improved algorithm. Just clone this repository, you need [SageMath](http://www.sagemath.org/) software. We use the SageMath v9.3 built from sources in WSL Ubuntu (Windows Subsystem for Linux). We also used Maple 2021. We additionally installed the following libraries:
- `tqdm`
- `memory-profiler`
To do that, one need to execute the following command:
```bash
> sage -pip install tqdm, memory_profiler
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
TODO
```

# Comparison to Groebner basis based algorithm

We compare our improved algorithm (e.g. containing reductions modulo prime numbers) to algorithm based on Groebner basis described in [[4]]().
Implementation of that algorithm can be found in [`algorithm_gb.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/algorithm_gb.py).
One can run this algorithm using script [`main.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/main.py) (as described above).

We compare time of calculating inverse mapping for two mappings using our improved approach and standard Groebner basis method.

Let us compare execution time for all algorithms executed to inverse mappings `EX19`:

```bash
TODO
```
The mapping `EX20`:
```bash
TODO
```

One can check these results himself. One can also check our paper _Algorithm for studying polynomial maps and reductions modulo prime number_.


# Hardware details

All examples were executed on Windows 10 machine with 16 GB RAM and intel i7 processor.


# Parallel computations


This repo contains first attempt of making the ABCH algorithm parallel. This simple proof of concept proves it is possible, and it really reduces time of execution
```bash
TODO
```

One can observe that parallel execution allows to reduce execution time.


# Bibliography

1. E. Adamus, P. Bogdan, T. Crespo and Z. Hajto, _An effective study of polynomial maps_, Journal of Algebra and Its Applications, Vol. 16, No. 08, 1750141 (2017)
2. E. Adamus, P. Bogdan, T. Crespo and Z. Hajto, _Pascal finite polynomial automorphisms_, Journal of Algebra and Its Applications, Vol. 18, No. 07, 1950124 (2019)
3. P. Bogdan, _Complexity of the inversion algorithm of polynomial mappings_, Schedae Informaticae, 2016, Volume 25, pages 209–225
4. A. van den Essen, _Polynomial Automorphisms and the Jacobian Conjecture_, Progress in Mathematics, 2000th Edition
5. E.-M. Hubbers. _The Jacobian Conjecture: Cubic homogeneous maps in dimension four_.  Master’s thesis, University of Nijmegen. [URL](http://www.cs.ru.nl/~hubbers/pubs/ivascriptie.pdf). Directed by A. van den Essen.
6. M. Bondt.  _Homogeneous keller maps_. Physical Review Letters, 01 2009.

