# Python program using topological sort to determine the order to complete all courses for a module in a proper order
from collections import defaultdict
from pyvis.network import Network
import pydot

# Class to represent a graph

pydot_graph = pydot.Dot('Module Selection', graph_type="graph")


def import_modules():
    modules = {}
    with open("modules.txt") as file:
        for line in file:
            (key, val) = line.split()
            modules[key] = int(val)

    return modules


def import_prerequisite_connections():
    prerequisite_connections = {}

    return prerequisite_connections


def display_optimal_order(order, nodes):
    node_order = []

    for item in order:
        node_order.append(list(nodes.keys())[list(nodes.values()).index(item)])

    return node_order


def generate_graph():
    pydot_graph.write('output.dot')

    net = Network(directed=True, notebook=True)
    net.from_DOT("output.dot")
    net.show("dot.html")
    net.show_buttons(filter_=["nodes"])


class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)  # dictionary containing adjacency List
        self.V = vertices  # No. of vertices

    def add_node(self, node, index):
        self.graph[node] = index
        pydot_graph.add_node(pydot.Node(index, label=node))

    # function to add an edge to graph
    def add_edge(self, u, v):
        self.graph[u].append(v)
        pydot_graph.add_edge(pydot.Edge(u, v))

    # A recursive function used by topologicalSort
    def topological_sort_util(self, v, visited, stack):

        # Mark the current node as visited.
        visited[v] = True

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)

        # Push current vertex to stack which stores result
        stack.append(v)

    # The function to do Topological Sort. It uses recursive
    # topological_sort_util()
    def topological_sort(self):
        # Mark all the vertices as not visited
        visited = [False] * self.V
        stack = []

        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for i in range(self.V):
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)

        # Print contents of the stack
        return stack[::-1]  # return list in reverse order


def main():
    # Import courses
    imported_modules = import_modules()

    graph = Graph(len(imported_modules))

    # Add Modules to Graph as nodes
    for index, module in enumerate(imported_modules):
        graph.add_node(module, index)

    # Add Edges to represent prerequisites
    graph.add_edge(imported_modules["Programming_1"], imported_modules["Programming_2"])
    graph.add_edge(imported_modules["Programming_2"], imported_modules["OOP"])
    graph.add_edge(imported_modules["College_Maths_1B"], imported_modules["Discreet_Maths"])
    graph.add_edge(imported_modules["Academic_Writing_I"], imported_modules["Academic_Writing_II"])
    graph.add_edge(imported_modules["College_Level_IT"], imported_modules["Database_Design"])
    graph.add_edge(imported_modules["College_Level_IT"], imported_modules["Web_Programming"])
    graph.add_edge(imported_modules["College_Level_IT"], imported_modules["CLD"])
    graph.add_edge(imported_modules["College_Maths_1B"], imported_modules["Intro_Stats"])
    graph.add_edge(imported_modules["OOP"], imported_modules["Data_Structures"])
    graph.add_edge(imported_modules["College_Level_IT"], imported_modules["SAD"])
    graph.add_edge(imported_modules["Discreet_Maths"], imported_modules["Physics"])
    graph.add_edge(imported_modules["Academic_Writing_I"], imported_modules["Ethics"])

    # Perform Topological Sort
    module_order = graph.topological_sort()

    # Display Optimal Order in which to do all courses
    print(display_optimal_order(module_order, imported_modules))

    # Generate Html File to represent graph
    generate_graph()


if __name__ == "__main__":
    main()
