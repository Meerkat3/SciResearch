#!/usr/bin/env python
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
import time
start_time = time.time()



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
for i in range (0,len(weights)):
    labelList.append(str(i))

# print(labelList)

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




# Create a nested dictionary from the ClusterNode's returned by SciPy
def add_node_height(node, parent , ht):
    # First create the new node and append it to its parent's children
    newNode = dict(node_id=node.id, children=[])
    parent["children"].append(newNode)

    if (ht < 31):
        # Recursively add the current node's children
        if node.left: add_node_height(node.left, newNode, ht+1)
        if node.right: add_node_height(node.right, newNode, ht+1)

# Initialize nested dictionary for d3, then recursively iterate through tree
d3Dendro = dict(children=[], name="Root1")
add_node(T, d3Dendro )


# Initialize nested dictionary for d3, then recursively iterate through tree
d3DendroDisp = dict(children=[], name="Root1")
add_node_height(T, d3DendroDisp , 0)

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
json.dump(d3DendroDisp, open(linkageType+"/d3-dendrogram.json", "w"), sort_keys=True, indent=4)


filenameIdx = 0
def createMergeJson(idx, dendoNodeList):
    G = nx.read_adjlist("adjListNumpy.txt")
    # print("\nNodelist from graph \n")
    # print(G.nodes())
    # G = nx.read_gml('lesmis.gml', label='id')
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

                unbrs = I.neighbors(u)
                vnbrs = I.neighbors(v)

                commonnbrs = [val for val in unbrs if val in vnbrs]

                # print("v :: "+v)
                # print(I.nodes())
                for nbr in commonnbrs:

                    edgeWeights[int(u)][int(nbr)] = edgeWeights[int(u)][int(nbr)] + edgeWeights[int(v)][int(nbr)]
                H.append(nx.contracted_nodes(I, u, v, self_loops=False))

    J = H.pop()
    H.append(J)

    L = nx.Graph()
    L.add_nodes_from(J.nodes())
    L.add_edges_from(J.edges())
    # print(J.nodes())
    # print(J.edges())
    # print(idx)


    # global filenameIdx
    print(len(J.nodes()))
    # if (len(J.nodes())< 41):
    # filenameIdx += 1
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
        jsonStr += "{\"source\": " + str(n[0]) + ", \"target\": " + str(n[1]) + ", \"distance\": " + str(edgeWeights[int(n[0])][int(n[1])])+"}"
        j += 1
        if j != len(G.edges()):
            jsonStr += ", "
    jsonStr += "]}"

    return jsonStr

# j = 0
# for dendoNodeList in dendoArr:
#     if dendoNodeList != []:
#         # for mergeNode in dendoNodeList:
#         #     print(mergeNode)
#         j += 1
#         if j != 1:
#             print(dendoNodeList)
#             createMergeJson(j, dendoNodeList)

j = 0
consolidatedArr = []

print("dendoArr[1] :: \n");
print(dendoArr[1]);
print("\n");

clusterList = dendoArr[1];

fileIdx = 0
for dendoNodeList in dendoArr:
    if dendoNodeList != []:
        # for mergeNode in dendoNodeList:
        #     print(mergeNode)
        j += 1
        if j != 1:
            removeList = []
            for supernode in dendoNodeList:
                for k in range(len(clusterList) - 1, -1, -1):
                    # print(clusterList[k])
                    # print(" :: ")
                    # print(supernode)
                    if set(clusterList[k]) <= set(supernode):
                        # print("identified subset :: " + str(k))
                        removeList.append(k)
            # print("removeList :: \n")
            # print(removeList)
            for k in reversed(sorted(removeList)):
                clusterList.pop(k)
            clusterList.extend(dendoNodeList)

            numNodes = 0
            clusteredNodes = 0
            for cluster in clusterList:
                clusteredNodes += len(cluster)

            numNodes = len(weights) - clusteredNodes + len(clusterList)


            print(numNodes)
            if(numNodes < 41 ):
                fileIdx += 1
                # print("dendoNodeList after extend :: \n")
                # print(dendoNodeList)
                print("\nclusterList   :: \n")
                print(clusterList)
                print("\n")
                createMergeJson(fileIdx, clusterList)


print("--- %s seconds ---" % (time.time() - start_time))

                        # if __name__ == '__main__':
#
#     G = nx.read_gml('lesmis.gml', label='id')
#     create_hc(G);