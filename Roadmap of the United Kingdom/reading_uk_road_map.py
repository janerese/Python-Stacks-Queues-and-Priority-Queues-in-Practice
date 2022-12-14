# Reading the DOT file (the UK road map) with the graph data type

from graph import City, load_graph

nodes, graph = load_graph("roadmap.dot", City.from_dict)

print(nodes["london"])
print(graph)

# Identifying immediate neighbors of a given city to find the available routes to follow when looking for the shortest path between two cities
for neighbor in graph.neighbors(nodes["london"]):
    print(neighbor.name)