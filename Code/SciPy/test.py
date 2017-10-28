import json
from pprint import pprint
import networkx as nx

from networkx.readwrite import json_graph

#
# with open('lemis.json') as data_file:
#     data = json.load(data_file)

#
# with open('lesmis.gml') as f:
#         js_graph = json.load(f)

# H = json_graph.node_link_graph(js_graph)

# s = json.dumps(data)
# print(s)
#
# H = json_graph.node_link_graph(s)

# print(H)

# pprint(js_graph)


G = nx.path_graph(4)
s = json.dumps(json_graph.node_link_data(G))

print(s)

with open("test.json", "w") as json_file:
    json_file.write(s)


# nx.write_gml(G, 'test.gml')
#
# H = nx.read_gml('lesmis.gml',label='id')
#
# print(H.nodes())
#
# M = nx.contracted_nodes(H, 4, 9, self_loops=False)
# #
# # nx.write_gml(M, 'contracted.gml')
# #
# print(M.nodes())

# G = nx.read_gml('lesmis.gml')
#
# print(G)