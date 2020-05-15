from sage.all import *

class FiniteFieldGraph:
    '''
    Class fields
      field: the Galois field upon which the graph is drawn
      field_order: the order of the Galois field
      relation: a function that determines whether 2 elements should share an
                 edge in the graph
      graph: the graph object storing the graph with a vertex set of the
              elements Galois field, and edges determined by the above relation
    '''

    def __init__(self, order, relation):
        '''
        Creates a graph of a finite field under a specific relation

        Parameters
          order, int: the order of the finite field
          relation, function : a function which returns whether two field
                                elements should have an edge

        Returns
          a FiniteFieldGraph object constructed from the field of the passed
           order under the relation

        Preconditions
          order is the power of some prime number
          
        Postconditions
          none additional
        '''
        super(FiniteFieldGraph, self).__init__()
        self.field = GF(order, "x")
        self.field_order = order
        self.relation = relation
        self.graph = Graph()
        self.construct_graph()

    def construct_graph(self):
        '''
        Adds vertices and edges to the graph based on the relation
        '''
        for elt in self.field:
            self.graph.add_vertex(elt)

        for x in self.field:
            for y in self.field:
                if self.relation(x, y) and (x != y):
                    self.graph.add_edge(x, y)
