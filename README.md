# Algorithm for studying polynomial maps and reductions modulo prime number

In [[1]]() we described an algorithm for inverting polynomial mappings. In [[3]]() complexity of this algorithm was estimated and moreover some aspects of the algorithm's implementation were discussed. Implementation of this algorithm can be found in this repository, in file [`algorithm_abch.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/algorithm_abch.py). This implementation works for both _Pascal finite_ and not _Pascal finite_ polynomial automorphism. Definition of _Pascal finite_ automorphisms can be found in [[2]]().

In _Algorithm for studying polynomial maps and reductions modulo prime number_ we explore properties of the algorithm and the class of Pascal finite maps while using Segre homotopy and reductions modulo prime number.  Additionally in this repository we present our code which illustrates improvements mad in the proposed algorithm.

We use fact that calculations performed over finite fields can be more effective (they are faster and use less memory) than those performed over fields of characteristic zero. We proceed as follows.
1. perform reduction modulo some set of prime numbers
2. inverse the reduced mappings using algorithm described in [[1]]()
3. retrieve global inverse using Chinese Reminder Theorem.

One can compare the base method with our improved algorithm. Just clone this repository, you only need [SageMath](http://www.sagemath.org/) software.
- File [`main-QQ.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/main-QQ.py) contains full program which inverts the mapping using our base approach. To run this program use the following command:
```bash
$ sage main-QQ.py
```
- File [`main-FF.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/main-FF.py) contains program which inverts the mapping using our improved approach.  To run this program use the following command:
```bash
$ sage main-FF.py
```
Difference in execution time can be easily observed.

## Notation

In this file we assume that `n`-variable polynomial mapping is a list of `n` `n`-variable polynomials:
```
F = (F_1, F_2, ..., F_n)
```
Every such a polynomial is a sum of terms. Every term is product of monomial and coefficient. The every polynomial `F_i` is in the following form:
```
F_i = X_i + H_i
```
Where `H_i` is a zero polynomial or `n`-variable polynomial
of lower degree (e.g. vanishing order) at least 2.
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

# Comparison

We compare our algorithm to algorithm based on Groebner basis described in [[4]](). 
Implementation of that algorithm can be found in [`algorithm_gb.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/algorithm_gb.py). 
One can run this algorithm using script [`main-GB.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/main-GB.py).

## Mapping 1

We compare time of calculating inverse mapping for two mappings using our improved approach and standard Groebner basis method.

We run program using our approach for the same mapping we used in previous comparison

```bash
$ sage main-FF.py 1
```

Then we run the program using Groebner basis algorithm for the same mapping:

```bash
$ sage main-GB.py 1
```

It appeared that the second program was being executing faster.

## Mapping 2

We run the same programs for the other mapping 

```bash
$ sage main-FF.py 2
```

and

```bash
$ sage main-GB.py 2
```

For this mapping our approach appeared to be more effective. 

One can check these results himself. One can also check our paper _Algorithm for studying polynomial maps and reductions modulo prime number_.

# Summary

The output from our scripts:

```bash
sage main-GB.py 1
Time necessary to inverse mapping: 5.191296815872192
(sage-sh) $ sage main-GB.py 2
Time necessary to inverse mapping: 22.258273124694824
(sage-sh) $ sage main-FF.py 1
Time necessary to inverse 3-reduced mapping: 0.0
Time necessary to inverse 5-reduced mapping: 110.29130840301514
Time necessary to inverse 7-reduced mapping: 169.9867227077484
Time necessary to inverse 11-reduced mapping: 328.91081261634827
Time necessary to inverse 13-reduced mapping: 350.0380210876465
Time necessary to inverse 17-reduced mapping: 335.9072127342224
Time necessary to inverse 19-reduced mapping: 341.8735542297363
Time necessary to inverse 23-reduced mapping: 400.78892397880554
Time necessary to inverse mapping: 2037.9245624542236
(sage-sh) $ sage main-FF.py 2
Time necessary to inverse 3-reduced mapping: 0.0
Time necessary to inverse 5-reduced mapping: 0.0060002803802490234
Time necessary to inverse 7-reduced mapping: 0.0060002803802490234
Time necessary to inverse 11-reduced mapping: 0.007000446319580078
Time necessary to inverse 13-reduced mapping: 0.009000539779663086
Time necessary to inverse 17-reduced mapping: 0.00800013542175293
Time necessary to inverse 19-reduced mapping: 0.010000467300415039
Time necessary to inverse 23-reduced mapping: 0.009000301361083984
Time necessary to inverse mapping: 0.14900851249694824
(sage-sh) $ sage main-QQ.py 1
Time necessary to inverse mapping: 10145.549292325974
(sage-sh) $ sage main-QQ.py 2
Time necessary to inverse mapping: 0.029001951217651367

```

# Bibliography

1. E. Adamus, P. Bogdan, T. Crespo and Z. Hajto, _An effective study of polynomial maps_, Journal of Algebra and Its Applications, Vol. 16, No. 08, 1750141 (2017)
2. E. Adamus, P. Bogdan, T. Crespo and Z. Hajto, _Pascal finite polynomial automorphisms_, Journal of Algebra and Its Applications, Vol. 18, No. 07, 1950124 (2019)
3. P. Bogdan, _Complexity of the inversion algorithm of polynomial mappings_, Schedae Informaticae, 2016, Volume 25, pages 209–225
4. A. van den Essen, _Polynomial Automorphisms and the Jacobian Conjecture_, Progress in Mathematics, 2000th Edition 
