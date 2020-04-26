"""
This file contains some helping functions
"""

import sys
from sage.all import *


def print_mapping(F, name='F'):
    """
    Function prints string representation of mapping F to standard output
    :param F: polynomial mapping
    :param name: name of mapping
    :return: None
    """
    R = F[0].parent()
    print('==================== Mapping ====================')
    print(R)
    for i in range(len(F)):
        print('{0}_{1}  = {2}'.format(name, i+1, F[i]))


def check_inversion(F, G, R):
    """
    Function checks if mapping G is an inverse of mapping F
    :param F: Polynomial mapping defined over ring R
    :param G: Polynomial mapping defined over ring R
    :param R: ring
    :return: None
    """
    for g, x in zip(G, R.gens()):
        assert g(F) == x

