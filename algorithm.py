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
    M = set(edgesM)

    setA, setB = bipartite.sets(G)
    groupANoM = setA.copy()
    groupBNoM = setB.copy()
    groupAWithM = set()
    groupBWithM = set()

    for u, v in list(M):
        if u in setA:
            groupANoM.remove(u)
            groupAWithM.add(u)
        if v in setB:
            groupBNoM.remove(v)
            groupBWithM.add(v)

    print("This is M: ", M)
    print("Group A\M: ", groupANoM)
    print("Group B\M: ", groupBNoM)
    print("Group A With M: ", groupAWithM)
    print("Group B With M: ", groupBWithM)
    return groupANoM, groupBNoM, groupAWithM, groupBWithM

def direct_graph(graph, group1, group2, group3, group4, M):
    directed_graph = defaultdict(list)

    for node in group1:  # nodes in A\M
        for neighbor in graph[node]:  # their neighbors
            if neighbor in group2:  # if neighbor is in B\M
                directed_graph[node].append(neighbor)  # add directed edge

    for u, v in M:  # for each edge in M
        if u in group3 and v in group2:  # if u is in A\M and v is in B\M
            directed_graph[v].append(u)  # add directed edge from B to A
        elif v in group3 and u in group2:  # if v is in A\M and u is in B\M
            directed_graph[u].append(v)  # add directed edge from B to A

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

def create_initial_matching(G, setA, setB):
    M = set()
    used = set()
    for u in setA:
        for v in G.neighbors(u):
            if v in setB and v not in used:
                M.add((u, v))
                used.add(u)
                used.add(v)
                break
    return M

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

    # Create an initial matching M
    setA, setB = bipartite.sets(G)
    M = create_initial_matching(G, setA, setB)
    draw_graph(G, pos, M)

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

            for edge in augmented_path_edges:
                u, v = edge
                if (u, v) in M:
                    M.remove((u, v))
                elif (v, u) in M:
                    M.remove((v, u))
                else:
                    M.add((u, v))
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
