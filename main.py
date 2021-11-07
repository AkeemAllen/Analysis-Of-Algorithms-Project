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

    for item in order:
        node_order.append(list(graph.keys())[list(graph.values()).index(item)])

    return node_order


def depth_first_search(v, visited, stack):
    visited[v] = True

    for i in graph[v]:
        if not visited[i]:
            depth_first_search(i, visited, stack)

    stack.append(v)


def topological_sort():
    visited = [False] * number_of_vertices
    stack = []

    for i in range(number_of_vertices):
        if not visited[i]:
            depth_first_search(i, visited, stack)

    return stack[::-1]


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


@app.route("/add-edge", methods=["POST"])
@cross_origin()
def add_edge():
    input_json = request.get_json(force=True)
    from_ = input_json["connection"]["from"]
    to = input_json["connection"]["to"]

    graph[graph[from_]].append(graph[to])
    pydot_graph.add_edge(pydot.Edge(graph[from_], graph[to]))

    return "Connection Added"


@app.route("/generate-graph")
@cross_origin()
def generate_graph():
    pydot_graph.write('output.dot')

    net = Network("500px", "100%", directed=True, notebook=True)
    net.from_DOT("output.dot")
    net.show("dot.html")

    with open("dot.html", "r") as file:
        html_file = file.read()

    soup = BeautifulSoup(html_file, "html.parser")
    return soup.prettify()


@app.route("/generate-optimal-order")
@cross_origin()
def generate_optimal_order():
    module_order = topological_sort()

    optimal_order = display_optimal_order(module_order)
    json_optimal_order = json.dumps(optimal_order, indent=4)
    return json_optimal_order


if __name__ == '__main__':
    app.run(port=5001)
