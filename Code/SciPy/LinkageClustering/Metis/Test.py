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


# with open('MetisIn.txt', 'w') as the_file:
#     the_file.write(str(len(G.nodes()))+" "+str(len(G.edges()))+'\n')
#
# with open('MetisIn.txt', 'a') as the_file:
#     for i in range(0, len(G.nodes())):
#         nbrs = G.neighbors(i)
#         for nbr in nbrs:
#             the_file.write(str(nbr+1)+ ' ')
#         the_file.write('\n')


def createMergeJson(dendoNodeList, idx):
    G = nx.read_gml('lesmis.gml', label='id')
    H = []
    H.append(G)
    for nodeList in dendoNodeList:
        if len(nodeList) > 1:
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


for k in range(2,21):
    with open('MetisIn.txt.part.'+str(k)) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    idx = [int(x.strip()) for x in content]

    # print(idx)
    nodelist = [[] for i in range(k)]

    for i in range(0, len(idx)):
        nodelist[idx[i]].append(i)

    print(nodelist)

    with open('lemis' + str(k) + '.json', "w") as json_file:
        json_file.write(getJsonStrGroup(G, idx))

    with open('lemisContracted' + str(k) + '.json', "w") as json_file:
        json_file.write(createMergeJson(nodelist, idx))
