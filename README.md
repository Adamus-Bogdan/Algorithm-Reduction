# Algorithm for studying polynomial maps and reductions modulo prime number

In article [[1]]() we described an algorithm for inverting polynomial mappings. In [[3]]() complexity of this algorithm was estimated. In [[3]]() some aspects of this algorithm's implementation were discussed. Implementation of this algorithm can be found in this repository, in file [`algorithm.py`](https://github.com/Adamus-Bogdan/Algorithm-Reduction/blob/master/algorithm.py). This implementation works for _Pascal finite_ and not _Pascal finite_ polynomial automorphism as well. Definition of _Pascal finite_ automorphisms can be found in [[2]]().

Article _Algorithm for studying polynomial maps and reductions modulo prime number_ contains description of some improvements of this algorithm and code in this repository ilustrates this improvmenents.

The main idea is to use fact that calculations performed over finite fields are much better (they are faster and use less memory) than those performed over infinite fields. Idea is:
1. to perform some reduction modulo some set of prime numbers
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


# Bibliography

1. E. Adamus, P. Bogdan, T. Crespo and Z. Hajto, _An effective study of polynomial maps_, Journal of Algebra and Its Applications, Vol. 16, No. 08, 1750141 (2017)
2. E. Adamus, P. Bogdan, T. Crespo and Z. Hajto, _Pascal finite polynomial automorphisms_, Journal of Algebra and Its Applications, Vol. 18, No. 07, 1950124 (2019)
3. P. Bogdan, _Complexity of the inversion algorithm of polynomial mappings_, Schedae Informaticae, 2016, Volume 25, pages 209–225
