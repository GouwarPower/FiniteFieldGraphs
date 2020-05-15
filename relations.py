# Author: John Gouwar
# File: relations.py
# Defines a generator for power-difference relations (i.e. is the difference of
# two elements an n^th power in the given field) and describes certain one-off
# relations

from sage.all import *

def power_relation_generator(power, combination, order):
    '''
    Generates a function that checks whether the difference of two elements in
     a Galois field of a specified order are can be expressed as a specific
     power of a single element

    Parameters
      power: the nth power that the generated relation will be based
      combination: a binary function that combines the two field elements into a
                    single field element
      order: the order of the Galois field in which the powers will be computed

    Returns
      relation, f: F_n x F_n x N -> bool: a function which returns whether the
        combination of two field elements can be expressed as the power of a
        single element in a field of order n

    Preconditions and Postconditions
      relation should only be used with fields of the same order that is passed
       to the generator
    '''
    # Precompute the necessary powers
    field = GF(order, "x")
    n_powers = list()
    for x in field:
        n_powers.append(x**power)
    n_powers = set(n_powers)

    # Define the relation to check against those powers
    def power_relation(x, y):
        residue = combination(x, y)
        zero_residue_check = residue != 0
        return ((residue in  n_powers) and zero_residue_check)

    return power_relation
