import networkx as nx
# import copy
from collections import defaultdict
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite

# The following function will build a simple graph


def BuildGraph():
    # Create an empty graph structure (a "null graph") with no nodes and no edges.
    G = nx.Graph()

    # Add nodes to the Graph
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)

    # Add edges to the Graph (pairs of nodes)
    G.add_edge(1, 2)
    G.add_edge(1, 3)

    # You can add nodes/edges to the Graph using lists as well
    G.add_nodes_from([4, 5, 6])
    G.add_edges_from([(4, 5), (5, 6)])
    G.add_edge(1, 6)
    # Draw the resulting Graph
    nx.draw(G, with_labels=True)

    if bipartite.is_bipartite(G):
        print("Graph is bipartite")
        setA, setB = bipartite.sets(G)
        print("Set 1: ", setA)
        print("Set 2: ", setB)

    # Finally, show the plot
    # plt.show()

    # Create the bipartite graph
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4, 5, 6])
    G.add_edges_from([(1, 2), (1, 3), (1, 6), (4, 5), (5, 6)])

    # Convert to directed graph
    DG = G.to_directed()

    if bipartite.is_bipartite(G):
        print("Graph is bipartite")
        setA, setB = bipartite.sets(G)
        print("Set 1: ", setA)
        print("Set 2: ", setB)
    else:
        print("The graph is not bipartite.")
    plt.show()


def DFS(directed_graph, start, end_set, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path.append(start)

    if start in end_set:
        return path

    for neighbour in directed_graph[start]:
        if neighbour not in visited:
            result_path = DFS(directed_graph, neighbour,
                              end_set, visited, path)
            if result_path:
                return result_path

    path.pop()
    return None


def augmenting_path(directed_graph, group1, group4):
    for node in group1:
        path = DFS(directed_graph, node, set(group4))
        if path:
            return path
    return None


def direct_graph(graph, group1, group2, group3, group4):
    directed_graph = defaultdict(list)

    groups = [set(group1), set(group2), set(group3), set(group4)]

    for i in range(3):  # for each group of nodes
        for node in groups[i]:
            for neighbor in graph[node]:
                if neighbor in groups[i+1]:  # if neighbor is in the next group
                    directed_graph[node].append(
                        neighbor)  # create a directed edge
    return directed_graph


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

    print("Group A\M: " , groupANoM)
    print("Group B\M: " , groupBNoM)
    print("Group A With M: " , groupAWithM)
    print("Group B With M: " , groupBWithM)
    return groupANoM, groupBNoM, groupAWithM, groupBWithM

def main():
    # Create the bipartite graph
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    G.add_edges_from([(1, 7), (1, 8), (2, 8), (2, 9), (3, 9), (3, 10), (4, 10), (4, 11), (5, 11), (5, 12), (6, 12), (6, 7)])


    nx.draw(G, with_labels=True)
    # Specify the group of edges to consider
    M = [(3,9)]
    while 1:
        print("New Start Loop")
        # Separate the bipartite graph into four groups
        groupANoM, groupBNoM, groupAWithM, groupBWithM = separate_bipartite_graph(G, M)
        directed_graph = direct_graph(G , groupANoM , groupBWithM , groupAWithM,groupBNoM)
        augmented_path = augmenting_path(directed_graph, groupANoM, groupBNoM)
        print("This is the Augmenting Path: ", augmented_path)
        if augmented_path:
            augmented_path_edges = [(augmented_path[i], augmented_path[i + 1]) for i in range(len(augmented_path) - 1)]
            if not M:
                M = augmented_path_edges
            else:
                for edge in augmented_path_edges:
                    u, v = edge
                    if any(((u, v) == (x, y) or (u, v) == (y, x)) for x, y in M):
                        M = [e for e in M if e != edge]  # Fix: Remove the edge from M
                    else:
                        M.append(edge)  # Fix: Append the edge to M


        else:
            print("No Augmenting Path Found, Exiting Loop")
            break


        print("This is the current Matching: " , M)
        print("End while iteration")
    # Show the plot
    print("Final matching M:", M)


if __name__ == "__main__":
    main()
