import networkx as nx

textline = '1 2 3 \n1 4 4\n2 4 '
fh = open('test.edgelist','w')
d = fh.write(textline)
fh.close()

G = nx.read_edgelist('test.edgelist', nodetype=int, data=(('weight',float),))
print(G.nodes())
print(G.edges(data = True))

print(G[1][2]['weight'])
print(G[2][4])
G[2][4]['weight']= 10
print(G[2][4])
print(G[1])

H = nx.contracted_nodes(G, 1, 2, self_loops=False)


print(H.nodes())
print(H.edges(data=True))

