# Using pygraphviz to read the sample DOt file (roadmap.dot)
import networkx as nx
print(nx.nx_agraph.read_dot("roadmap.dot"))

# This is printed: MultiGraph named 'Cities in the United Kingdom' with 70 nodes and 137 edges