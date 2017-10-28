#!/usr/bin/python

# Load required modules
import pandas as pd
import scipy.spatial
import scipy.cluster
import numpy as np
import json
import matplotlib.pyplot as plt
import functools
import networkx as nx
from networkx.readwrite import json_graph

# Example data: gene expression
geneExp = {'genes': ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76"],
           'exp1': [-153.61350767373872, -178.81683102405182, -106.47037090489454, -96.97131130965386, -188.79044747999072, -195.63361395310764, -167.49730822492728, -197.6712672726601, -192.3164547884889, -189.2032605887982, -4.90206035844503, -23.980463769319737, -62.32904828511515, -18.40702943917438, -32.65795787145551, -59.7710516454193, -35.28511479993335, -76.03767648989876, -74.51289477721845, -90.75681934856946, -97.01754386815281, -57.60683401494254, -107.78468788600293, -67.5727630368314, -14.60004874708656, 19.298461259112358, 23.55908020448588, -18.70558342643693, -79.15665379295847, -62.5831428901978, -79.49009621463728, -54.926262423817406, -46.62582519588268, -53.54630572519164, -26.098992212145898, -66.98475984978093, -43.17529090874181, -47.0762351216003, -69.43644809106183, 76.76140499564151, -7.776128460898534, 65.48475597299897, 21.7893492132959, 3.0427701437097383, -76.28117288745675, -122.22164448098007, 92.96900593631742, 94.11145895738849, 95.0419460333584, 59.27953755565993, 29.17250606000878, 60.388500492312815, 92.33826226331476, 73.01395081015855, 92.74542081190276, 105.38135323516433, 110.8526521972619, 154.77261110522792, 117.3219508497147, 168.73324306146267, 178.94563729233332, 157.57461457537573, 151.3743197951473, 185.15864810751157, 128.06057145778448, 185.87815473932238, 166.8689260545572, 191.30020092027695, 14.54926617623866, 0.11964321318456335, 36.71042484759652, 27.917391173852526, -27.611563834747567, 111.02942015556029, 83.11577179945563, 44.62443163140196, 152.78119588257553]
,
           'exp2': [86.95554145281945, 120.62809977890439, 50.31992689845783, 70.21780005972931, 104.5280744984741, 85.80285560876611, 125.97609794287736, 97.57426542046785, 73.45531027561496, 115.57931954434936, 53.2189171085891, 20.746148071491042, -58.0274166601947, 58.923505232337384, 58.20915478282677, 29.510825946592487, -177.12276656857185, -215.91837925905165, -240.8102958019552, -201.36961874911728, -234.04400844215002, -225.51518268680985, -214.4056191182733, -134.4205269521361, -60.486332117428056, -41.650739209094624, -66.44103614698113, -19.450732523317395, -8.439442861798566, 44.463293450084976, -108.40181436928542, -66.24956112822787, 51.611375656125716, -5.161875527945953, 106.93336254267636, 90.62428274162706, 95.2620189477435, 119.03734651495822, 110.15345271367342, -59.81219869474531, -77.05537728715224, -18.452035578735604, -76.61623470413588, -26.403544089515155, 22.85630659928161, -12.977270411244547, 154.99681690250335, 109.85860583728272, 47.00215385970525, -42.09410919502962, -85.77576838729061, -69.62117645038772, -103.57851229619156, -110.82999415499732, -70.82080942852228, -15.647879351954037, -51.32487457151714, 11.138683785082963, 41.21111349526551, 44.71373325323221, 83.09310203811494, 62.54127213853898, 35.882439079380546, 60.260809227975464, 63.30830507985422, 40.47417578706403, 99.31102075921879, -3.6011983976488846, 5.342305366952755, -1.836064353535262, 8.289483455619314, 26.180331239459463, -39.68390456189229, 91.45761111413424, 90.26465434990402, -5.634784118943841, 81.74003173879488]

           }
df = pd.DataFrame(geneExp)

# Determine distances (default is Euclidean)
dataMatrix = np.array(df[['exp1', 'exp2']])
distMat = scipy.spatial.distance.pdist(dataMatrix)

# Cluster hierarchicaly using scipy
clusters = scipy.cluster.hierarchy.linkage(distMat, method='single')
T = scipy.cluster.hierarchy.to_tree(clusters, rd=False)

# Create dictionary for labeling nodes by their IDs
labels = list(df.genes)
id2name = dict(zip(range(len(labels)), labels))

# Draw dendrogram using matplotlib to scipy-dendrogram.pdf
scipy.cluster.hierarchy.dendrogram(clusters, labels=labels, orientation='right')
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
    if len(leafNames) > currLength :
        diff = len(leafNames)- currLength
        # print(diff)
        i = 0
        while(i < diff):
            dendoArr.append([])
            i += 1
        # print(dendoArr)
        currLength = len(leafNames)
        # print(len(leafNames))
        # print(currLength)

    # print(leafNames);
    dendoArr[len(leafNames)-1].append(leafNames)

    # print(dendoArr)
    return leafNames


# print(dendoArr)

# print(len(dendoArr))

label_tree(d3Dendro["children"][0])

# Output to JSON
json.dump(d3Dendro, open("d3-dendrogram.json", "w"), sort_keys=True, indent=4)

def createMergeJson(idx , dendoNodeList):
    G = nx.read_gml('lesmis.gml', label='id')
    H= []
    H.append(G)
    for nodeList in dendoNodeList :
        print(nodeList)
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
    print("J's Nodes :: \n");
    print(J.nodes())

    jsonStr = getJsonStr(J)
    print(jsonStr)

    # Creates the file with contracted nodes
    with open('lemisContracted'+str(idx)+'.json', "w") as json_file:
        json_file.write(jsonStr)
    # nx.write_gml(J, 'lemisContracted'+str(idx)+'.gml')



def getJsonStr(G):
    jsonStr = "{ " + "\"nodes\"" + ":[ "
    j = 0
    for n in G.nodes():
        jsonStr += "{\"id\": "+str(n)+"}"
        j += 1
        if j != len(G.nodes()):
            jsonStr += ", "
    jsonStr += "], \"links\": ["

    j = 0
    for n in G.edges():
        jsonStr += "{\"source\": "+str(n[0])+", \"target\": "+str(n[1])+"}"
        j += 1
        if j != len(G.edges()):
            jsonStr += ", "
    jsonStr += "]}"

    return jsonStr


# j = 0
# for dendoNodeList in dendoArr :
#     if dendoNodeList != [] :
#         # for mergeNode in dendoNodeList:
#         #     print(mergeNode)
#         j += 1
#         if j != 1 :
#             print("dendo Node list :: "+str(j)+"\n");
#             print(dendoNodeList)
#             createMergeJson( j, dendoNodeList)


j = 0
consolidatedArr = []

print("dendoArr[1] :: \n");
print(dendoArr[1]);
print("\n");

clusterList = dendoArr[1];


for dendoNodeList in dendoArr :
    if dendoNodeList != [] :
        # for mergeNode in dendoNodeList:
        #     print(mergeNode)
        j += 1
        if j != 1 :
            removeList = []
            for supernode in dendoNodeList:
                for k in range(len(clusterList)-1, -1 , -1) :
                    print(clusterList[k])
                    print(" :: ")
                    print(supernode)
                    if set(clusterList[k]) <= set(supernode):
                        print("identified subset :: " + str(k))
                        removeList.append(k)
            print("removeList :: \n")
            print(removeList)
            for k in reversed(sorted(removeList)):
                clusterList.pop(k)
            clusterList.extend(dendoNodeList)
            print("dendoNodeList after extend :: \n")
            print(dendoNodeList)

            print("clusterList   :: \n")
            print(clusterList)
            print("\n")
            createMergeJson( j, clusterList)
