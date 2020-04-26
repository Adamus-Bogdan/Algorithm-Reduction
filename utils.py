import sys
from sage.all import *

def print_mapping(F, name='F'):
    R = F[0].parent()
    print('==================== Mapping ====================')
    print(R)
    for i in range(len(F)):
        print('{0}_{1}  = {2}'.format(name, i+1, F[i]))

def check_inversion(F, G, R):
    for g, x in zip(G, R.gens()):
        assert g(F) == x

