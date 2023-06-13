import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from networkx.algorithms import bipartite

# Function to draw the graph with optional highlighting of matching edges and augmenting path
def draw_graph(G, pos, M=[], path=[]):
    print("Drawing Graph")
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

    # Draw non-matching edges in blue, matching edges in red, and augmenting path edges in green dashed lines
    nx.draw_networkx_edges(G, pos, edgelist=non_M_edges, edge_color='blue', width=2)
    nx.draw_networkx_edges(G, pos, edgelist=M_edges, edge_color='red', width=2)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='green', style='dashed', width=2)

    plt.show(block=False)
    plt.pause(2)

# Function to separate the bipartite graph into different groups based on the current matching
def separate_bipartite_graph(G, edgesM):
    M = set(edgesM)

    setA, setB = bipartite.sets(G)
    groupANoM = setA.copy()
    groupBNoM = setB.copy()
    groupAWithM = set()
    groupBWithM = set()

    # Categorize nodes based on their group and whether they are in the matching M
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

# Function to create a directed graph based on the current matching
def direct_graph(graph, group1, group2, group3, group4, M):
    directed_graph = defaultdict(list)
    for node in group1:
        for neighbour in graph[node]:
            if neighbour in group2:
                directed_graph[node].append(neighbour)
    for node in group2:
        for neighbour in graph[node]:
            if neighbour in group3:
                directed_graph[node].append(neighbour)
    for node in group3:
        for neighbour in graph[node]:
            if neighbour in group4:
                directed_graph[node].append(neighbour)
    for node in group4:
        for neighbour in graph[node]:
            if neighbour in group1:
                directed_graph[node].append(neighbour)
    return directed_graph

# Function to find an augmenting path in the directed graph
def augmenting_path(directed_graph, group1, group4):
    print("Searching for augmenting path")
    for node in group1:
        path = DFS(directed_graph, node, group4, visited=set(), path=[])
        if path:
            return path
    return None

# Depth-first search to find an augmenting path in the directed graph
def DFS(directed_graph, start, end_set, visited, path):
    visited.add(start)
    path.append(start)
    if start in end_set:
        return path
    for neighbour in directed_graph[start]:
        if neighbour not in visited:
            result_path = DFS(directed_graph, neighbour, end_set, visited.copy(), path.copy())
            if result_path:
                return result_path
    return None

# Function to create the initial matching by greedily selecting edges
def create_initial_matching(G, setA, setB, pos):
    M = set()
    used = set()
    for u in setA:
        for v in G.neighbors(u):
            if v in setB and v not in used:
                M.add((u, v))
                used.add(u)
                used.add(v)
                draw_graph(G, pos, M)
                break
    return M

# Function to update the current matching based on the augmenting path
def update_augmenting(M, augmented_path_edges):
    for edge in augmented_path_edges:
        u, v = edge
        if (u, v) in M:
            M.remove((u, v))
        elif (v, u) in M:
            M.remove((v, u))
        else:
            M.add((u, v))

# Function to build the graph and find the maximum matching
def build_graph():
    G = nx.Graph()

    edges = edges_entry.get().split()
    for edge in edges:
        u, v = edge.split(',')
        G.add_edge(u, v)

    pos = nx.spring_layout(G)
    draw_graph(G, pos)

    # Create an initial matching M
    setA, setB = bipartite.sets(G)
    M = create_initial_matching(G, setA, setB, pos)
    draw_graph(G, pos, M)

    while True:
        groupANoM, groupBNoM, groupAWithM, groupBWithM = separate_bipartite_graph(G, M)
        directed_graph = direct_graph(G, groupANoM, groupBWithM, groupAWithM, groupBNoM, M)
        augmented_path = augmenting_path(directed_graph, groupANoM, groupBNoM)
        print("This is the Augmenting Path: ", augmented_path)

        if augmented_path:
            augmented_path_edges = [(augmented_path[i], augmented_path[i + 1]) for i in range(len(augmented_path) - 1)]

            draw_graph(G, pos, M, augmented_path_edges)
            update_augmenting(M, augmented_path_edges)
            draw_graph(G, pos, M)
        else:
            print("No Augmenting Path Found, Exiting Loop")
            break
        print("This is the current Matching: ", M)
        print("End while iteration")

    print("Final matching M:", M)

# Create the tkinter GUI
# The code starts here
root = tk.Tk()
root.title("Graph Builder")

edges_label = tk.Label(root, text="Add Edges (comma-separated):")
edges_label.pack()

edges_entry = tk.Entry(root)
edges_entry.pack()

build_graph_button = tk.Button(root, text="Build Graph", command=build_graph)
build_graph_button.pack()

root.mainloop()
