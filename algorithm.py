import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from networkx.algorithms import bipartite

def draw_graph(G, pos, M=[], path=[]):
    plt.clf()
    # Draw nodes with a yellow color
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='yellow')

    # Create labels for nodes
    labels = {node: str(node) for node in G.nodes()}

    # Draw labels on the nodes
    nx.draw_networkx_labels(G, pos, labels=labels, font_color='black')

    non_M_edges = [e for e in G.edges() if e not in M and tuple(reversed(e)) not in M]
    M_edges = [e for e in M]
    path_edges = [e for e in path]

    nx.draw_networkx_edges(G, pos, edgelist=non_M_edges, edge_color='blue', width=2)
    nx.draw_networkx_edges(G, pos, edgelist=M_edges, edge_color='red', width=2)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='black', style='dashed', width=2)

    plt.show(block=False)
    plt.pause(1)

def separate_bipartite_graph(G, edgesM):
    M = set()
    for u, v in edgesM:
        M.add(u)
        M.add(v)

    setA, setB = bipartite.sets(G)
    groupANoM = setA.copy()
    groupBNoM = setB.copy()
    groupAWithM = set()
    groupBWithM = set()

    for u in list(G.nodes()):
        if u in setA and u in M:
            groupANoM.remove(u)
        if u in setB and u in M:
            groupBNoM.remove(u)

    print("This is M: ", M)
    for u, v in edgesM:
        if u in setA:
            groupAWithM.add(u)
        if v in setB:
            groupBWithM.add(v)

    print("Group A\M: ", groupANoM)
    print("Group B\M: ", groupBNoM)
    print("Group A With M: ", groupAWithM)
    print("Group B With M: ", groupBWithM)
    return groupANoM, groupBNoM, groupAWithM, groupBWithM

def direct_graph(graph, group1, group2, group3, group4, M):
    directed_graph = defaultdict(list)

    M = set(M)

    groups = [group1.union(group2), group2, group3, group3.union(group4)]

    for i in range(3):  # for each group of nodes
        for node in groups[i]:
            for neighbor in graph[node]:
                if neighbor in groups[i+1]:  # if neighbor is in the next group
                    if not ((node, neighbor) in M or (neighbor, node) in M):  # ignore edges from M
                        directed_graph[node].append(neighbor)  # create a directed edge

    # specifically check if there are direct connections between group1 and group4
    for node in group1:
        for neighbor in graph[node]:
            if neighbor in group4:
                if not ((node, neighbor) in M or (neighbor, node) in M):  # ignore edges from M
                    directed_graph[node].append(neighbor)  # create a directed edge

    return directed_graph

def augmenting_path(directed_graph, group1, group4):
    for node in group1:
        path = DFS(directed_graph, node, set(group4))
        if path:
            return path
    return None

def DFS(directed_graph, start, end_set, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = [start]
    else:
        path = path + [start]  # create a new path

    visited.add(start)

    if start in end_set:
        return path

    for neighbour in directed_graph[start]:
        if neighbour not in visited:
            result_path = DFS(directed_graph, neighbour, end_set, visited, path)
            if result_path:
                return result_path

    return None

def build_graph():
    G = nx.Graph()

    # Add nodes to the Graph
    nodes = node_entry.get().split()
    G.add_nodes_from(nodes)

    # Add edges to the Graph
    edges = edges_entry.get().split()
    for edge in edges:
        u, v = edge.split(',')
        G.add_edge(u, v)

    pos = nx.spring_layout(G)
    draw_graph(G, pos)

    M = []
    while True:
        print("New Start Loop")
        groupANoM, groupBNoM, groupAWithM, groupBWithM = separate_bipartite_graph(G, M)
        directed_graph = direct_graph(G, groupANoM, groupBWithM, groupAWithM, groupBNoM, M)
        augmented_path = augmenting_path(directed_graph, groupANoM, groupBNoM)
        print("This is the Augmenting Path: ", augmented_path)

        if augmented_path:
            augmented_path_edges = [(augmented_path[i], augmented_path[i + 1])
                                    for i in range(len(augmented_path) - 1)]

            draw_graph(G, pos, M, augmented_path_edges)

            if not M:
                M = augmented_path_edges
            else:
                for edge in augmented_path_edges:
                    u, v = edge
                    if any(((u, v) == (x, y) or (v, u) == (x, y)) for x, y in M):
                        M = [e for e in M if e != edge and e != (v, u)]
                    else:
                        M.append(edge)
            draw_graph(G, pos, M)
        else:
            print("No Augmenting Path Found, Exiting Loop")
            break
        print("This is the current Matching: ", M)
        print("End while iteration")

    print("Final matching M:", M)

root = tk.Tk()
root.title("Graph Builder")

num_nodes_label = tk.Label(root, text="Number of Nodes:")
num_nodes_label.pack()

num_nodes_entry = tk.Entry(root)
num_nodes_entry.pack()

num_edges_label = tk.Label(root, text="Number of Edges:")
num_edges_label.pack()

num_edges_entry = tk.Entry(root)
num_edges_entry.pack()

node_label = tk.Label(root, text="Add Node (space-separated):")
node_label.pack()

node_entry = tk.Entry(root)
node_entry.pack()

edges_label = tk.Label(root, text="Add Edges (comma-separated):")
edges_label.pack()

edges_entry = tk.Entry(root)
edges_entry.pack()

build_graph_button = tk.Button(root, text="Build Graph", command=build_graph)
build_graph_button.pack()

root.mainloop()
