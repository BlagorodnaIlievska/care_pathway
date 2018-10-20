import networkx as nx


def create_graph_per_patient(patient, column1, column2):
    patient[column1] = patient[column2].shift(-1)
    patient = patient[:-1]
    # Build your graph
    g = nx.from_pandas_edgelist(patient, column1, column2, create_using=nx.DiGraph())
    return g


def closure_transitive(g):

    h = nx.transitive_closure(g)
    return h


def reduction_transitive(g):

    h = nx.dag.transitive_reduction(g)
    return h


def write_graph_file(graph_name, graph, location, addition):

    graph_file = ''
    graph_name = graph_name
    graph_file = graph_file + str(graph_name)
    number_of_nodes = graph.number_of_nodes()
    graph_file = graph_file + '\n' + str(number_of_nodes)
    number_of_edges = graph.number_of_edges()
    graph_file = graph_file + ' ' + str(number_of_edges)
    nodes = list(graph.nodes)
    for i in range(0, (len(nodes))):
        # print(nodes[i])
        edge_list = list(graph.neighbors(nodes[i]))
        n_indexes = []
        for e in edge_list:
            index = nodes.index(e)
            n_indexes.append(index)
        # print(n_indexes)
        graph_file = graph_file + '\n' + str(nodes[i]) + '\n'  # + ' '.join(str(n_indexes))
        if len(n_indexes):

            # node_index_str = ''
            for i in n_indexes:
                graph_file = graph_file + str(i) + ' '
        #     #print(i)
    # print(graph_file)
    f = open(location + str(graph_name) + '_' + addition + '.gr', 'w')
    f.write(graph_file)
    f.close()


def save_collection_graphs(original_df, members, id, location, addition):

    for m in members:
        member = original_df[(original_df[id] == m)]
        member = member[[id, 'Category', 'Procedure_start']]
        g = create_graph_per_patient(member)
        g = closure_transitive(g)
        graph_name = member[id].unique()[0]
        write_graph_file(graph_name, g, location, addition)


def most_common_subgraph(g, h):

    matching_graph = nx.DiGraph()

    for n1, n2, attr in h.edges(data=True):
        if g.has_edge(n1, n2):
            matching_graph.add_edge(n1, n2, weight=1)

    graphs = list(nx.weakly_connected_component_subgraphs(matching_graph))

    mcs_length = 0
    mcs_graph = nx.DiGraph()
    for i, graph in enumerate(graphs):

        if len(graph.nodes()) > mcs_length:
            mcs_length = len(graph.nodes())
            mcs_graph = graph

    return mcs_graph


def make_symmetric(matrix):

    for i in range(1, len(matrix)):
        for j in reversed(range(len(matrix) - len(matrix[i]))):
            matrix[i].insert(0, matrix[j][i])

    return matrix


def make_graphs(df, members):

    all_members_info = []
    for_which_mem = []
    for i in range(0, len(members)):

        first = df[(df['Person_ID'] == members[i])]
        for_which_mem.append(first['Person_ID'].unique()[0])
        g = create_graph_per_patient(first)
        g = closure_transitive(g)
        all_members_info.append(g)

    return all_members_info
