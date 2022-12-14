# Using pygraphviz to read the sample DOt file (roadmap.dot)
import networkx as nx
from graph import *
print(nx.nx_agraph.read_dot("roadmap.dot"))
# This should be printed: MultiGraph named 'Cities in the United Kingdom' with 70 nodes and 137 edges

# networkx represents graph nodes using textual identifiers that can optionally have an associated dictionary of attributes
graph = nx.nx_agraph.read_dot("roadmap.dot")
print(graph.nodes["london"])
# This should be printed: {'country': 'England', 'latitude': '51.507222', 'longitude': '-0.1275', 'pos': '80,21!', 'xlabel': 'City of London', 'year': '0'}