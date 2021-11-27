# Group Members
# Akeem Allen - 1706357
# Norval Excell - 1903461
# Malique Malcolm - 1807910

import json

import pydot
from pyvis.network import Network
from flask import Flask, request
from collections import defaultdict
from flask_cors import cross_origin
from bs4 import BeautifulSoup

app = Flask(__name__)

modules = {}
graph = defaultdict(list)
pydot_graph = pydot.Dot('Module Selection', graph_type="graph")
current_node_position = 0
number_of_vertices = 0


def display_optimal_order(order):
    node_order = []

    try:
        for item in order:
            node_order.append(list(graph.keys())[list(graph.values()).index(item)])
    except ValueError:
        return []

    return node_order


def depth_first_search(v, visited, stack):
    visited[v] = True

    for i in graph[v]:
        if not visited[i]:
            depth_first_search(i, visited, stack)

    stack.append(v)


# Algorithm pulled from https://www.geeksforgeeks.org/topological-sorting/
def topological_sort():
    visited = [False] * number_of_vertices
    stack = []

    for i in range(number_of_vertices):
        if not visited[i]:
            depth_first_search(i, visited, stack)

    return stack[::-1]


# Adds Nodes To The Graph as well as pydot
@app.route("/add-node", methods=["POST"])
@cross_origin()
def add_node():
    global current_node_position
    global number_of_vertices

    input_json = request.get_json(force=True)
    graph[input_json["node"]] = current_node_position
    pydot_graph.add_node(pydot.Node(current_node_position, label=input_json["node"]))
    current_node_position = current_node_position + 1
    number_of_vertices = number_of_vertices + 1
    return "Module Added"


# Adds Edges To The Graph as well as pydot
@app.route("/add-edge", methods=["POST"])
@cross_origin()
def add_edge():
    input_json = request.get_json(force=True)
    from_ = input_json["connection"]["from"]
    to = input_json["connection"]["to"]

    graph[graph[from_]].append(graph[to])
    pydot_graph.add_edge(pydot.Edge(graph[from_], graph[to]))

    return "Connection Added"


# Generates graph using html for visualization
@app.route("/generate-graph")
@cross_origin()
def generate_graph():
    pydot_graph.write('output.dot')

    net = Network("500px", "100%", directed=True, notebook=True)
    net.from_DOT("output.dot")
    net.save_graph("dot.html")

    with open("dot.html", "r") as file:
        html_file = file.read()

    soup = BeautifulSoup(html_file, "html.parser")
    return soup.prettify()


# Resets graph by deleting output and dot file
@app.route("/clear-graph")
@cross_origin()
def clear_graph():
    import os
    global modules, graph, pydot_graph, current_node_position, number_of_vertices
    modules = {}
    graph = defaultdict(list)
    pydot_graph = pydot.Dot('Module Selection', graph_type="graph")
    current_node_position = 0
    number_of_vertices = 0

    if os.path.exists("dot.html"):
        os.remove("dot.html")
    else:
        print("The file does not exist")

    if os.path.exists("output.dot"):
        os.remove("output.dot")
    else:
        print("The file does not exist")
    return "Graph Reset"


# Uses the topological sort to generate
# the optimal order in which to do modules
@app.route("/generate-optimal-order")
@cross_origin()
def generate_optimal_order():
    module_order = topological_sort()

    optimal_order = display_optimal_order(module_order)
    json_optimal_order = json.dumps(optimal_order, indent=4)
    return json_optimal_order


# Clears application after initialization
@app.route("/")
@cross_origin()
def app_started():
    global modules, graph, pydot_graph, current_node_position, number_of_vertices
    modules = {}
    graph = defaultdict(list)
    pydot_graph = pydot.Dot('Module Selection', graph_type="graph")
    current_node_position = 0
    number_of_vertices = 0

    return "Started"


# Initializes application on port 5001
if __name__ == '__main__':
    app.run(port=5001, debug=True)
