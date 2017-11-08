
from collections import defaultdict
import networkx as nx
import numpy
import math
from scipy.cluster import hierarchy
from scipy.spatial import distance
import matplotlib.pyplot as plt
import scipy.cluster
import functools
import json


G = nx.read_gml('lesmis.gml', label='id')
# create_hc(G);
#
#
# def create_hc(G):
#     """Creates hierarchical cluster of graph G from distance matrix"""
path_length=nx.all_pairs_shortest_path_length(G)


# for x in path_length:
#     print(x)
distances=numpy.zeros((len(G),len(G)))
for u,p in path_length:
    for v,d in p.items():
        distances[u][v]=d

# print(distances)
# print(path_length)




with open("0050432.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
weights = [x.strip() for x in content]

corrM =numpy.zeros((len(weights), len(weights)))
edgeWeights =numpy.zeros((len(weights), len(weights)))


adj_ids = [ [x for x in range(len(weights))] for x in range(len(weights))]

for i in range(0,len(adj_ids)):
    adj_ids[i].remove(i)
    adj_ids[i].insert(0,i)


for i in range(0,len(weights)):
    cols = weights[i].split()
    for j in range(0, len(cols)):
        corrM[i][j] =  float(cols[j])
        edgeWeights[i][j] = math.sqrt(1 - float(cols[j]))

print(corrM)
print(edgeWeights)

adjFile = open('adjList.txt', 'w')



for row in adj_ids:
    # print(row)
    adjFile.write("%s\n" % row)

numpy.savetxt("adjListNumpy.txt" , adj_ids, delimiter=' ', newline='\n', fmt='%d')


G=nx.read_adjlist("adjListNumpy.txt")


print(G.nodes())
print(G.edges())