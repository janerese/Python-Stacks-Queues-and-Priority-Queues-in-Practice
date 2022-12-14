# Define a custom data type representing a city in the road map

# Necessary modues
from typing import NamedTuple
import networkx as nx
from queues import Queue

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