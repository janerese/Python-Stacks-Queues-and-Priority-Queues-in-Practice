# Reading the DOT file (the UK road map) with the graph data type

from graph import City, load_graph

nodes, graph = load_graph("roadmap.dot", City.from_dict)

print(nodes["london"])
print(graph)

