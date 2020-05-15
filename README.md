# FiniteFieldGraphs
This code was originally developed for my final project for Grinnell's MAT-322: Algebraic Graph theory. It's purpose is to aid in the development of conjectures for graphs arising from the relationship of elements of finite fields.

## Dependencies
This project requires a working copy of SageMath 9.0, installed from the binaries provided by SageMath.

## FiniteFieldGraph class
Instances of the FiniteFieldGraph class take a field order and a relation between field elements that determines whether or not two elements should share an edge, and produce an object which contains the field, its order, the relation used, and the actual graph generated as members.
Example:
```
from sage.all import *
from FiniteFieldGraph import FiniteFieldGraph as FFG

# The complete graph on 8 vertices
k_8 = FFG(8, lambda x, y: x-y != 0)

# The Paley Graph P_9
p_9 = FFG(9, lambda x, y: (x-y)**(4) % 9 == 1)

# The 5-regular Clebsch Graph
c_16 = FFG(16, lambda x, y: (x-y)**(5) % 16 == 1)
```

## gcg_experiment.py
This is the actual file used for developing the conjectures present in the paper. It loops through various powers of 2, generates the field corresponding to that power, finds the divisors of the order of the unit group, for each divisor, d, creates a graph on that field where the relation is determined by whether or not the difference of two elements is a d-th residue, and then checks if the graph is both connected and strongly regular. It then outputs these results to either a text file or the console.

To run it simply run the command `sage -python gcg_experiment.py`. It will prompt you for a starting power of 2 (e.g. for 16 = 2^4, you would put 4), the final power of two you would like to test (e.g. for 16384 = 2^14, you would put 14), and an output text file (if left blank, output will be printed to the console). This process spawns as many subprocesses as your computer has CPU power, so this experiment will consume a great number of resources for any power of 2 greater than 10.   


## Final Paper
The final paper for this class that I created, "On the Strong Regularity of Cubic Paley Graphs on Finite Fields of Even Order," is contained in the repository as MAT-322-Final-Paper.pdf. Section 2 contains the basic mathematical concepts for the paper, section 3 contains discussion of how the code was used, and sections 4+5 work towards proving the ultimate result of the paper.  
