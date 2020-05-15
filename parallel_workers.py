from sage.all import *

import relations as rel
from FiniteFieldGraph import FiniteFieldGraph as FFG

def power_relation_graph_worker(power, comb, order, graph_dicts):
    # Creates a relation that checks whether the difference of two
    # elements are a residue of power fact in the field
    relation = rel.power_relation_generator(power, comb, order)

    # Generates the FFG object based on the relation and store it
    field_graph_obj = FFG(order, relation)
    field_graph_dict = {
        "field_order" : field_graph_obj.field_order,
        "graph" : field_graph_obj.graph,
        "residue_power" : power
    }
    graph_dicts.append(field_graph_dict)

def connected_srg_worker(field_graph_dict, checked_graphs):
    connected = field_graph_dict['graph'].is_connected()
    strongly_regular = False
    if connected:
        strongly_regular = field_graph_dict['graph'].is_strongly_regular(True)

    new_field_graph_dict = dict(field_graph_dict)
    new_field_graph_dict['connected'] = connected
    new_field_graph_dict['srg'] = strongly_regular

    checked_graphs.append(new_field_graph_dict)
