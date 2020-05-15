from math import *
import functools
import sys

class OutputWriter:
    '''
    A class which wraps stdout, stderr and file writing so that the where
    particular data is to be written does not have to change how the user writes
    it
    '''
    def __init__(self, output_loc):
        self.output_loc = output_loc
        if output_loc == "stdout":
            self.output = sys.stdout
        elif output_loc == "stderr":
            self.output = sys.stderr
        else:
            self.output = open(output_loc, "a")

    def write(self, text):
        self.output.write(text + "\n")

    def close(self):
        if not (self.output_loc in ["stdout", "stderr"]):
            self.output.close()

def non_trivial_factors(n):
    '''
    Returns a set of non-trivial (i.e. not 1 and itself) factors of natural
    number
    '''
    # Create a list of pairs of factors n
    fact_list = [[i, n // i] for i in range(2, ceil((sqrt(n)))+5) if n % i == 0]

    # If n is prime, fact_list will be empty, which will break reduce
    if fact_list == list():
        return set(list())

    # Reduce the pairs of factors, remove duplicates, and sort by size
    return sorted(set(functools.reduce(lambda a, b: a + b, fact_list)))
