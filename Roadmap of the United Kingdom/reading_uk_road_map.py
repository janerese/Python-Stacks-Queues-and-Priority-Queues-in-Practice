# Reading the DOT file (the UK road map) with the graph data type

import networkx as nx
from graph import (
    City,
    load_graph,
    breadth_first_traverse,
    breadth_first_search as bfs,
    shortest_path,
    connected,
    depth_first_traverse,
    depth_first_search as dfs,
    dijkstra_shortest_path
)

# Testing the class City and from_dict() and load_graph() function
print("First Testing: Using networkx module:")
nodes, graph = load_graph("roadmap.dot", City.from_dict)

print(nodes["london"])
print("\n")
print(graph)

# Identifying immediate neighbors of a given city to find the available routes to follow when looking for the shortest path between two cities
print("\n2nd testing: Identify immediate neighbors")
for neighbor in graph.neighbors(nodes["london"]):
    print(neighbor.name)

# Include the weights of the connecting edges, such as distances or the estimated travel times
print("\n3rd testing: Neighbors with possible weights of the connecting edges")
for neighbor, weights in graph[nodes["london"]].items():
    print(weights["distance"], neighbor.name)

# The neighbors are always listed in the same order in which you defined them in the DOT file. To sort them by one or more weights, you can use the following code snippet:
print("\n4th testing: Sorting the neighbors")
def sort_by(neighbors, strategy):
    return sorted(neighbors.items(), key=lambda item: strategy(item[1]))

def by_distance(weights):
    return float(weights["distance"])

for neighbor, weights in sort_by(graph[nodes["london"]], by_distance):
    print(f"{weights['distance']:>3} miles, {neighbor.name}")

# Breadth-First Search Using a FIFO Queue
# Calling the nx.bfs_tree() function on your graph to reveal the breadth-first order of traversal
print("\n5th testing: Find any place in the United Kingdom that has been granted city status in the twentieth century, starting your search in Edinburgh")
def is_twentieth_century(year):
    return year and 1901 <= year <= 2000

nodes, graph = load_graph("roadmap.dot", City.from_dict)
for node in nx.bfs_tree(graph, nodes["edinburgh"]):
    print("📍", node.name)
    if is_twentieth_century(node.year):
        print("Found:", node.name, node.year)
        break
else:
    print("Not found")

# To ensure consistent resutls, sort the neighbors according to some criteria
print("6th testing: Visit cities with a higher latitude first")
def order(neighbors):
    def by_latitude(city):
        return city.latitude
    return iter(sorted(neighbors, key=by_latitude, reverse=True))

for node in nx.bfs_tree(graph, nodes["edinburgh"], sort_neighbors=order):
    print("📍", node.name)
    if is_twentieth_century(node.year):
        print("Found:", node.name, node.year)
        break
else:
    print("Not found")

# Testing the breadth-first search and traversal implementations
print("\n7th testing: Breadth-first search and traversal implementation")
def is_twentieth_century(city):
    return city.year and 1901 <= city.year <= 2000

nodes, graph = load_graph("roadmap.dot", City.from_dict)
city = bfs(graph, nodes["edinburgh"], is_twentieth_century)
print(city.name)
print("\n")
for city in breadth_first_traverse(graph, nodes["edinburgh"]):
    print(city.name)

# Shortest Path Using Breadth-First Traversal
# Revealing the shortest path between two cities
print("\n8th testing: Using networkx to reveal all the shortest paths between two cities")
nodes, graph = load_graph("roadmap.dot", City.from_dict)

city1 = nodes["aberdeen"]
city2 = nodes["perth"]

for i, path in enumerate(nx.all_shortest_paths(graph, city1, city2), 1):
    print(f"{i}.", " → ".join(city.name for city in path))

# Queue-based implementation of the shortest path
# When you call the queue-based implementation of the shortest path, you get the same results as with networkx
print("\n9th testing: Queue-based implementation of the shortest path")
print(" → ".join(city.name for city in shortest_path(graph, city1, city2)))

def by_latitude(city):
    return -city.latitude

print(" → ".join(
    city.name
    for city in shortest_path(graph, city1, city2, by_latitude)
))

# Testing the breadth-first travelsal implementation of whther two nodes remain connected or not
print("\n10th testing: Using breadth-first traversal to check whether two nodes remain connected or not")
print(connected(graph, nodes["belfast"], nodes["glasgow"]))

print(connected(graph, nodes["belfast"], nodes["derry"]))

# Replacing nx.bfs_tree() with nx.dfs_tree() from earling example to compare the difference
print("\n11th testing: Difference when nx.bfs_tree() is replaced with nx.dfs_tree() ")
def is_twentieth_century(year):
    return year and 1901 <= year <= 2000

nodes, graph = load_graph("roadmap.dot", City.from_dict)
for node in nx.dfs_tree(graph, nodes["edinburgh"]):
    print("📍", node.name)
    if is_twentieth_century(node.year):
        print("Found:", node.name, node.year)
        break
else:
    print("Not found")

# Testing the breadth_first_search() and depth_first_search() functions call search() with the corresponding traversal strategy
print("\n12th testing: Using refactored breadth_first_search() and new depth_first_search()")
def is_twentieth_century(city):
    return city.year and 1901 <= city.year <= 2000

nodes, graph = load_graph("roadmap.dot", City.from_dict)
city = dfs(graph, nodes["edinburgh"], is_twentieth_century)
print(city.name)
print("\n")
for city in depth_first_traverse(graph, nodes["edinburgh"]):
    print(city.name)

# Testing  Dijkstra’s algorithm
print("\n13th testing: Dijkstra’s algorithm:")
nodes, graph = load_graph("roadmap.dot", City.from_dict)
city1 = nodes["london"]
city2 = nodes["edinburgh"]

def distance(weights):
    return float(weights["distance"])

for city in dijkstra_shortest_path(graph, city1, city2, distance):
    print(city.name)

# Networkx implementation
print("\nCompare to Networkx implementation:")
def weight(node1, node2, weights):
    return distance(weights)

for city in nx.dijkstra_path(graph, city1, city2, weight):
    print(city.name)