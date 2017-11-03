#!/usr/bin/env python
# encoding: utf-8

from collections import defaultdict
import networkx as nx
import numpy
from scipy.cluster import hierarchy
from scipy.spatial import distance
import matplotlib.pyplot as plt
import scipy.cluster
import functools
import json

from scipy.cluster.vq import vq, kmeans, whiten



G = nx.read_gml('lesmis.gml', label='id')
# create_hc(G);
#
#
path_length=nx.all_pairs_shortest_path_length(G)
distances=numpy.zeros((len(G),len(G)))
for u,p in path_length.items():
    for v,d in p.items():
        distances[u][v]=d
        # print(d)

print(distances)
whitened = whiten(distances)

# print(whitened)

def createMergeJson(dendoNodeList, idx):
    G = nx.read_gml('lesmis.gml', label='id')
    H = []
    H.append(G)
    for nodeList in dendoNodeList:
        # print(nodeList)
        u = nodeList[0]
        # print("u :: "+ u)
        for x in range(1, len(nodeList)):
            I = H.pop()
            v = nodeList[x]
            # print("v :: "+v)
            # print(I.nodes())
            H.append(nx.contracted_nodes(I, int(u), int(v), self_loops=False))
    J = H.pop()
    H.append(J)

    L = nx.Graph()
    L.add_nodes_from(J.nodes())
    L.add_edges_from(J.edges())
    # print(J.nodes())
    # print(J.edges())
    # print(idx)

    jsonStr = getJsonStr(J, idx)

    return jsonStr
    # print(jsonStr)
    # attrsG = dict(id='id', source='source', target='target', key='id')

    ###### print(json.dumps(json_graph.node_link_data(L)))


def getJsonStr(G, idx):
    jsonStr = "{ " + "\"nodes\"" + ":[ "
    j = 0
    for n in G.nodes():
        jsonStr += "{\"id\": " + str(n)+ ", \"group\" :" + str(idx[n]) +"}"
        j += 1
        if j != len(G.nodes()):
            jsonStr += ", "
    jsonStr += "], \"links\": ["

    j = 0
    for n in G.edges():
        jsonStr += "{\"source\": " + str(n[0]) + ", \"target\": " + str(n[1]) + "}"
        j += 1
        if j != len(G.edges()):
            jsonStr += ", "
    jsonStr += "]}"

    return jsonStr



def getJsonStrGroup(G , arr):
    jsonStr = "{ " + "\"nodes\"" + ":[ "
    j = 0
    for n in G.nodes():
        jsonStr += "{\"id\": " + str(n) + ", \"group\" :" + str(arr[n]) +"}"
        j += 1
        if j != len(G.nodes()):
            jsonStr += ", "
    jsonStr += "], \"links\": ["

    j = 0
    for n in G.edges():
        jsonStr += "{\"source\": " + str(n[0]) + ", \"target\": " + str(n[1]) + "}"
        j += 1
        if j != len(G.edges()):
            jsonStr += ", "
    jsonStr += "]}"

    return jsonStr



def makeClusters(n):
    # computing K-Means with K clusters
    K = n
    centroids,_ = kmeans(whitened,K)
    # assign each sample to a cluster
    idx,_ = vq(whitened,centroids)


    nodelist = [[] for i in range(K)]

    for i in range(0, len(idx)):
        nodelist[idx[i]].append(i)


    print(nodelist)


    with open('lemis' + str(n) + '.json', "w") as json_file:
        json_file.write(getJsonStrGroup(G, idx))


    with open('lemisContracted' + str(n) + '.json', "w") as json_file:
        json_file.write(createMergeJson(nodelist, idx))


for i in range(1,21):
    makeClusters(i)

# group_data = {}
#
# for i in range(0, len(idx)):
#     group_data.update({i: idx[i]})
#
# print(group_data)
#
# nx.set_node_attributes(G, 'group', group_data)
#
# print(G.nodes())