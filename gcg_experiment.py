from sage.all import *
import multiprocessing as multi


import tools
import parallel_workers


def generate_generalized_clebsch_graphs(power):
    '''
    Generates graphs from Galois fields of even order by determining whether two
     elements of the field subtracted from one another are a particular
     residue. Each graph is based on one residue of the factors of the order of
     the field's unit group.

    Parameters
        power, int: the power that 2 will be raised to for the order of the
                     Galois field

    Returns
        checked_graphs, list: A list of dictionaries summarizing a
                               FiniteFieldGraph object with the keys
                               "field_order"(int),
                               "graph"(Sage GenericGraph object),
                               "residue_power"(int), "connected"(bool),
                               "strongly_regular"(either False, or SRG params)

    Preconditions
        none additional

    Postconditions
        Note that this function has two places where it attempts to run in
         parallel
    '''
    # Creates manager that can be shared by subprocesses, FiniteFieldGraph
    # objects are stored as dicts which retain some of the members of the FFG
    # objects, but since the FFG objects cannot be pickled in their entirety,
    # they cannot be passes to and from subprocesses
    graph_dicts_manager = multi.Manager()
    graph_dicts = graph_dicts_manager.list()

    # Galois field order and the order of its unit group
    order = 2**power
    unit_group_order = order - 1

    # All factors (not 1 and itself) of the order of the field's unit group
    factors = tools.non_trivial_factors(unit_group_order)

    # next loop if unit group order is prime (i.e. has no factors)
    if not factors:
        return

    # Generate the graphs for each factor of the unit group in parallel
    jobs = []
    for fact in factors:
        p = multi.Process(target=parallel_workers.power_relation_graph_worker,
                          args=(fact, (lambda x,y: x-y), order, graph_dicts))
        jobs.append(p)
        p.start()

    # Have all of the jobs reintroduce their side effects (i.e. add the
    # graph_dict they generated to graph_dicts)
    for proc in jobs:
        proc.join()

    # Check the graphs for connectedness and strong regularity
    return check_graphs(graph_dicts)


def check_graphs(graph_dicts):
    '''
    Checks if a list graphs, stored as graph_dicts (defined above), are both
    connected and strongly regular. This process is done in parallel. 
    '''
    checked_graphs_manager = multi.Manager()
    checked_graphs = checked_graphs_manager.list()
    jobs = []
    for ffg_dict in graph_dicts:
        p = multi.Process(target=parallel_workers.connected_srg_worker,
                          args=(ffg_dict, checked_graphs))
        jobs.append(p)
        p.start()

    for p in jobs:
        p.join()

    return checked_graphs


def write_results(checked_graphs, file):
    '''
    Writes the results of batch of graphs that have been checked for
    connectedness and strong regularity
    '''
    # Checks if a file was passed and creates a writer for that file;
    # otherwise, creates a writer to stdout
    if file:
        writer = tools.OutputWriter(file)
    else:
        writer = tools.OutputWriter("stdout")

    # Do nothing if empty list of dicts
    if not checked_graphs:
        writer.close()
        return

    for ffg_dict in checked_graphs:
        # Format output based on connectedness
        base = f"GF({ffg_dict['field_order']}), "+\
               f"Residue Power: {ffg_dict['residue_power']}"
        if ffg_dict['connected']:
            output =  base + f", SRG: {ffg_dict['srg']}"
        else:
            output = base + " is not connected"

        writer.write(output)

    writer.close()


def gen_and_write(power, file):
    '''
    Glues the process of generating a graphs for a particular power of 2 and
    writing their output
    '''
    checked_graphs = generate_generalized_clebsch_graphs(power)
    write_results(checked_graphs, file)

if __name__ == "__main__":
    starting_power = eval(input("What is the starting power of 2?: "))
    ending_power = eval(input("What is the ending power of 2?: "))
    file = input("Where would you like the output (leave blank for console): ")
    for pow in range(starting_power, ending_power+1):
        gen_and_write(pow, file)
