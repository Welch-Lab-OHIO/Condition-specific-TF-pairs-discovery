import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


"""
================================================================================
FigS10_cluster_networks.py
Script written by: Michael Cooney

Date: July 15, 2025

--------------------------------------------------------------------------------
NOTE: this description is not yet complete.  The usage example still needs to
be explained further.
--------------------------------------------------------------------------------

This script generates a network and sub-networks based off features that were
manually clustered by their appearance in the upset plot of figure 4i.

Sub-networks show the features in a cluster and all features within 1 degree of
separation from members of the cluster.

Usage example:
>>> python FigS10_cluster_networks.py cluster_list_csv 4_set_venn_list

================================================================================
"""

color_map = {
    'SD': '#88ccee',
    'S3': '#ddcc77',
    'S3SD': '#cc6677',
    'HC_SD': '#aa4499',
    'HC_S3SD': '#882255',
    'HC_S3': '#332288',
    'SD_S3SD': '#117733',
    'SD_S3': '#44aa99',
    'S3_S3SD': '#88ccee',
    'SD_S3_S3SD': '#ddcc77',
    'HC_S3_S3SD': '#fe7e0f',
    'HC_SD_S3': '#fc59a3',
    'HC_SD_S3_S3SD': '#ffd400',
}

def remove_nan(values: list[str]) -> list[str]:
    return(list(i for i in values if str(i) != 'nan'))

def strings_to_ints(data: list[(str, str)]) -> list[int]:
    value_map = {}
    index = 0
    for edge in data:
        if edge[0] in value_map:
            pass
        else:
            value_map[edge[0]] = index
            index += 1
        if edge[1] in value_map:
            pass
        else:
            value_map[edge[1]] = index
            index += 1

    int_data = list(map(lambda s: (value_map[s[0]], value_map[s[1]]), data))
    return int_data

def make_sub_network(subject: list[str], key: str, network_data: dict[str: list[str]]) -> None:
    # Initialize graph values.  These values will be added to/incremented as we go
    edges = []
    nodes = []
    clusters = []

    # For each tf in the cluster, find it's partners in the entire dataset
    for tf in subject:
        if tf not in nodes:
            nodes.append(tf)
            clusters.append(key)
        partners = network_data[tf]
        for i in partners:
            # 'partners' data has form (tf, venn_region, cluster_name)
            if i[0] not in nodes:
                nodes.append(i[0])
                clusters.append(i[2])
            edges.append((tf, i[0]))
            
    # Replace strings with integers in edges
    int_edges = strings_to_ints(edges)
    print(int_edges)
    # Make the graph
    graph = ig.Graph(len(nodes), int_edges)
    graph['title'] = key
    graph.vs['name'] = nodes
    graph.vs['cluster'] = clusters

    graph.write_gml(f'{key}_network.gml')


def make_network(clusters: {str: list[str]}, \
                 network_data: dict[str: list[str]], \
                 title: str) -> None:
    edges = []
    nodes = []

    # These will be used for coloring the graphs
    edge_destinations = []
    edge_origins = []
    cluster_ids = []

    edge_colors = []

    for cluster in clusters:
        for tf in clusters[cluster]:
            if tf not in nodes:
                nodes.append(tf)
                cluster_ids.append(cluster)
            partners = network_data[tf]
            for partner in partners:
                if partner[0] not in nodes:
                    nodes.append(partner[0])
                    cluster_ids.append(partner[2])
                edges.append((tf, partner[0]))
                edge_destinations.append(partner[2])
                edge_origins.append(cluster)

                edge_colors.append('x')
                if cluster == 'HC_SD_S3_S3SD' or partner[2] == 'HC_SD_S3_S3SD':
                    edge_colors[-1] = ('HC_SD_S3_S3SD')
                if cluster == 'HC_SD_S3' or partner[2] == 'HC_SD_S3':
                    edge_colors[-1] = ('HC_SD_S3')
                if cluster == 'HC_S3_S3SD' or partner[2] == 'HC_S3_S3SD':
                    edge_colors[-1] = ('HC_S3_S3SD')
                if cluster == 'SD_S3_S3SD' or partner[2] == 'SD_S3_S3SD':
                    edge_colors[-1] = ('SD_S3_S3SD')
                if cluster == 'S3_S3SD' or partner[2] == 'S3_S3SD':
                    edge_colors[-1] = ('S3_S3SD')
                if cluster == 'SD_S3' or partner[2] == 'SD_S3':
                    edge_colors[-1] = ('SD_S3')
                if cluster == 'SD_S3SD' or partner[2] == 'SD_S3SD':
                    edge_colors[-1] = ('SD_S3SD')
                if cluster == 'HC_S3' or partner[2] == 'HC_S3':
                    edge_colors[-1] = ('HC_S3')
                if cluster == 'HC_S3SD' or partner[2] == 'HC_S3SD':
                    edge_colors[-1] = ('HC_S3SD')
                if cluster == 'HC_SD' or partner[2] == 'HC_SD':
                    edge_colors[-1] = ('HC_SD')
                if cluster == 'S3SD' or partner[2] == 'S3SD':
                    edge_colors[-1] = ('S3SD')
                if cluster == 'S3' or partner[2] == 'S3':
                    edge_colors[-1] = ('S3')
                if cluster == 'SD' or partner[2] == 'SD':
                    edge_colors[-1] = ('SD')
                

    int_edges = strings_to_ints(edges)
    # Make the graph
    graph = ig.Graph(len(nodes), int_edges)
    graph['title'] = 'TF Pair Network'
    graph.vs['name'] = nodes
    graph.vs['cluster'] = cluster_ids
    graph.es['destination'] = edge_destinations
    graph.es['origin'] = edge_origins
    graph.es['edge_colors'] = edge_colors

    graph.write_gml(f'{title}.gml')



if __name__ == '__main__':
    # File containing the clusters as column headers and the constituent TFs as
    # the data
    clusters = pd.read_csv(sys.argv[1])
    print(f'reading file {sys.argv[1]}')

    # File containing the TF pairs as they were assorted into the 4-way Venn
    # diagram
    pairs = pd.read_csv(sys.argv[2])
    print(f'reading file {sys.argv[2]}')

    cluster_dict = {}
    pairs_dict = {}
    adjacency = {}
    label_dict = {}

    # Put clusters in a dict
    for cluster in clusters:
        cluster_dict[cluster] = remove_nan(clusters[cluster].values)
        # Label the TF with a color
        for tf in cluster_dict[cluster]:
            label_dict[tf] = cluster


    # Repeat above for Venn regions
    for region in pairs:
        values_list = remove_nan(pairs[region].values)
        if len(values_list) == 0:
            continue
        pairs_dict[region] = remove_nan(pairs[region].values)


    # Make an adjacency matrix for individual TFs using pairs from above
    for region in pairs_dict:
        for pair in pairs_dict[region]:
            tfs = pair.split('_')
            if tfs[0] in adjacency:
                adjacency[tfs[0]].append((tfs[1], region, label_dict[tfs[1]]))
            else:
                adjacency[tfs[0]] = [(tfs[1], region, label_dict[tfs[1]])]

            if tfs[0] == tfs[1]:
                continue

            if tfs[1] in adjacency:
                adjacency[tfs[1]].append((tfs[0], region, label_dict[tfs[0]]))
            else:
                adjacency[tfs[1]] = [(tfs[0], region, label_dict[tfs[0]])]

    make_network(cluster_dict, adjacency, 'colored_edges')
