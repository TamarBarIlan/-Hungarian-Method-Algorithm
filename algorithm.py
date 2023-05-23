import networkx as nx
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

# The following function will seperate the bipartite graph to 4 groups


def separate_bipartite_graph(G, edgesM):
    
    M = set()
    for u, v in edgesM:
        M.add(u)
        M.add(v)
    
    setA, setB = bipartite.sets(G)
    groupANoM = setA.copy()
    groupBNoM = setB.copy()
    groupAWithM = setA.copy()
    groupBWithM = setB.copy()

    for u in list(G.nodes()):
        if u in setA and u in M:
            groupANoM.remove(u)
        if u in setB and u in M:
            groupBNoM.remove(u)

    print("This is M: ", M)
    print("~~~~~~~~~~~~~~~~~~~~~")
    for u in list(G.nodes()):
        if u in setA and u not in M:
            groupAWithM.remove(u)
        if u in setB and u not in M:
            groupBWithM.remove(u)

    print(groupANoM)
    print(groupBNoM)
    print(groupAWithM)
    print(groupBWithM)
    return groupANoM, groupBNoM, groupAWithM, groupBWithM


def main():
    # Create the bipartite graph
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4, 5, 6])
    G.add_edges_from([(1, 2), (1, 3), (1, 6), (4, 5), (5, 6)])
    nx.draw(G, with_labels=True)
    # Specify the group of edges to consider
    M = {(1, 3)}

    # Separate the bipartite graph into four groups
    groupANoM, groupBNoM, groupAWithM, groupBWithM = separate_bipartite_graph(G, M)

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()
