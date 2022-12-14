# Define a custom data type representing a city in the road map

# Necessary modues
from typing import NamedTuple
import networkx as nx
from queues import Queue
from collections import deque

# Extend a named tuple to ensure that node objects are hashable, which is required by networkx
class City(NamedTuple):
    name: str
    country: str
    year: int | None
    latitude: float
    longitude: float

    @classmethod
    # The .from_dict() class method takes a dictionary of attributes extracted from a DOT file and returns a new instance of your City class
    def from_dict(cls, attrs):
        return cls(
            name=attrs["xlabel"],
            country=attrs["country"],
            year=int(attrs["year"]) or None,
            latitude=float(attrs["latitude"]),
            longitude=float(attrs["longitude"]),
        )

# To take advantage of the new class, create a new graph instance and take note of the mapping of node identifiers to city instances
def load_graph(filename, node_factory):
    graph = nx.nx_agraph.read_dot(filename)
    nodes = {
        name: node_factory(attributes)
        for name, attributes in graph.nodes(data=True)
    }
    return nodes, nx.Graph(
        (nodes[name1], nodes[name2], weights)
        for name1, name2, weights in graph.edges(data=True)
    )

# Breadth-First Search Using a FIFO Queue
# The functions does not allow sorting the neighbors in a particular order
# def breadth_first_traverse(graph, source):
#     queue = Queue(source)
#     visited = {source}
#     while queue:
#         yield (node := queue.dequeue())
#         for neighbor in graph.neighbors(node):
#             if neighbor not in visited:
#                 visited.add(neighbor)
#                 queue.enqueue(neighbor)

# def breadth_first_search(graph, source, predicate):
#     for node in breadth_first_traverse(graph, source):
#         if predicate(node):
#             return node

# One possible solution for allowing sorting the neighbors in a particular order
def breadth_first_traverse(graph, source, order_by=None):
    queue = Queue(source)
    visited = {source}
    while queue:
        yield (node := queue.dequeue())
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key=order_by)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)

def breadth_first_search(graph, source, predicate, order_by=None):
    for node in breadth_first_traverse(graph, source, order_by):
        if predicate(node):
            return node

# This new function takes another node as an argument and optionally lets you order the neighbors using a custom strategy
# It also defines an empty dictionary, which you populate when visiting a neighbor by associating it with the previous node on your path
# All key-value pairs in this dictionary are immediate neighbors without any nodes between them
def shortest_path(graph, source, destination, order_by=None):
    queue = Queue(source)
    visited = {source}
    previous = {}
    while queue:
        node = queue.dequeue()
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key=order_by)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)
                previous[neighbor] = node
                if neighbor == destination:
                    return retrace(previous, source, destination)

# To recreate the shortest path between your source and destination, you can iteratively look up the dictionary built earlier when you traversed the graph with the breadth-first approach
def retrace(previous, source, destination):
    path = deque()

    current = destination
    while current != source:
        path.appendleft(current)
        current = previous.get(current)
        if current is None:
            return None

    path.appendleft(source)
    return list(path)
