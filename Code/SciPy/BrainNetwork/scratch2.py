# encoding: utf-8

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


with open("0050432.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
weights = [x.strip() for x in content]

corrM =numpy.zeros((len(weights), len(weights)))
edgeWeights =numpy.zeros((len(weights), len(weights)))

for i in range(0,len(weights)):
    cols = weights[i].split()
    for j in range(0, len(cols)):
        corrM[i][j] =  float(cols[j])
        edgeWeights[i][j] = math.sqrt(1 - float(cols[j]))

print(corrM)
print(edgeWeights)

adj_ids = [ [x for x in range(len(weights))] for x in range(len(weights))]

for i in range(0,len(adj_ids)):
    adj_ids[i].remove(i)
    adj_ids[i].insert(0,i)


numpy.savetxt("adjListNumpy.txt" , adj_ids, delimiter=' ', newline='\n', fmt='%d')

G=nx.read_adjlist("adjListNumpy.txt")

linkageType = 'weighted'
# Create hierarchical cluster
Y=distance.squareform(edgeWeights)
Z=hierarchy.weighted(Y)


cutree = scipy.cluster.hierarchy.cut_tree(Z, n_clusters=5)

print(len(cutree))