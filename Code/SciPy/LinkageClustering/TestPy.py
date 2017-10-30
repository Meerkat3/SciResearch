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



G = nx.read_gml('lesmis.gml', label='id')
# create_hc(G);
#
#
# def create_hc(G):
#     """Creates hierarchical cluster of graph G from distance matrix"""
path_length=nx.all_pairs_shortest_path_length(G)
distances=numpy.zeros((len(G),len(G)))
for u,p in path_length.items():
    for v,d in p.items():
        distances[u][v]=d
        # print(d)


linkageType = 'weighted'
# Create hierarchical cluster
Y=distance.squareform(distances)
Z=hierarchy.weighted(Y)
# Creates HC using farthest point linkage
# This partition selection is arbitrary, for illustrive purposes

# membership=list(hierarchy.fcluster(Z,t=1.15))
# # Create collection of lists for blockmodel
#
# partition=defaultdict(list)
# for n,p in zip(list(range(len(G))),membership):
#     partition[p].append(n)
# return list(partition.values())


T = scipy.cluster.hierarchy.to_tree(Z, rd=False)

labelList = []
for i in range (0,77):
    labelList.append(str(i))

print(labelList)

# Create dictionary for labeling nodes by their IDs
labels = list(labelList)
id2name = dict(zip(range(len(labels)), labels))

# Draw dendrogram using matplotlib to scipy-dendrogram.pdf
scipy.cluster.hierarchy.dendrogram(Z, labels=labels, orientation='right')
plt.savefig("scipy-dendrogram.png")

# Create a nested dictionary from the ClusterNode's returned by SciPy
def add_node(node, parent):
    # First create the new node and append it to its parent's children
    newNode = dict(node_id=node.id, children=[])
    parent["children"].append(newNode)

    # Recursively add the current node's children
    if node.left: add_node(node.left, newNode)
    if node.right: add_node(node.right, newNode)

# Initialize nested dictionary for d3, then recursively iterate through tree
d3Dendro = dict(children=[], name="Root1")
add_node(T, d3Dendro)

dendoArr = []
currLength = 0

# Label each node with the names of each leaf in its subtree
def label_tree(n):
    # If the node is a leaf, then we have its name
    if len(n["children"]) == 0:
        leafNames = [id2name[n["node_id"]]]

    # If not, flatten all the leaves in the node's subtree
    else:
        leafNames = functools.reduce(lambda ls, c: ls + label_tree(c), n["children"], [])

    # Delete the node id since we don't need it anymore and
    # it makes for cleaner JSON


    del n["node_id"]

    # Labeling convention: "-"-separated leaf names
    n["name"] = name = "-".join(sorted(map(str, leafNames)))

    # print(leafNames if len(leafNames) == 2 else "")
    global currLength
    global dendoArr
    if len(leafNames) > currLength:
        diff = len(leafNames) - currLength
        # print(diff)
        i = 0
        while (i < diff):
            dendoArr.append([])
            i += 1
        # print(dendoArr)
        currLength = len(leafNames)
        # print(len(leafNames))
        # print(currLength)

    # print(leafNames);
    dendoArr[len(leafNames) - 1].append(leafNames)

    # print(dendoArr)
    return leafNames

# print(dendoArr)

# print(len(dendoArr))

label_tree(d3Dendro["children"][0])

# Output to JSON
json.dump(d3Dendro, open(linkageType+"/d3-dendrogram.json", "w"), sort_keys=True, indent=4)

def createMergeJson(idx, dendoNodeList):
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

    jsonStr = getJsonStr(J)
    # print(jsonStr)
    # attrsG = dict(id='id', source='source', target='target', key='id')

    ###### print(json.dumps(json_graph.node_link_data(L)))
    global linkageType
    with open(linkageType+'/lemis' + str(idx) + '.json', "w") as json_file:
        json_file.write(jsonStr)


        # nx.write_gml(J, 'lemisContracted'+str(idx)+'.gml')

def getJsonStr(G):
    jsonStr = "{ " + "\"nodes\"" + ":[ "
    j = 0
    for n in G.nodes():
        jsonStr += "{\"id\": " + str(n) + "}"
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

j = 0
for dendoNodeList in dendoArr:
    if dendoNodeList != []:
        # for mergeNode in dendoNodeList:
        #     print(mergeNode)
        j += 1
        if j != 1:
            print(dendoNodeList)
            createMergeJson(j, dendoNodeList)


# if __name__ == '__main__':
#
#     G = nx.read_gml('lesmis.gml', label='id')
#     create_hc(G);