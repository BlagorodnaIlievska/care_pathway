from controlers.graphs import *
import pandas as pd


def calculate_distance_matrix(all_graphs, members):
    all_members_info = []
    for_which_mem = []
    for i in range(0, len(members)):
        one_mem_info = []

        for_which_mem.append(members[i])
        g = all_graphs[i]

        for j in range(i, (len(members))):
            h = all_graphs[j]

            match = most_common_subgraph(g, h)
            if ((g.number_of_nodes() == 0) & (h.number_of_nodes() == 0)):
                distance = 1
            else:
                distance = round(float(1 -
                                       (match.number_of_nodes() / max(g.number_of_nodes(), h.number_of_nodes()))), 2)

            distance = round(float(distance), 3)
            one_mem_info.append(float(distance))

        all_members_info.append(one_mem_info)

    all_members_info = make_symmetric(all_members_info)
    all_info = pd.DataFrame(all_members_info, columns=for_which_mem)
    all_info['id'] = for_which_mem
    return all_members_info, for_which_mem

    return df
