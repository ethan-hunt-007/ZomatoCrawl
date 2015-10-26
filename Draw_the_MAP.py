import networkx as nx
import matplotlib.pyplot as plt


G=nx.Graph()

f=open(r'C:\Users\Jayant\Desktop\Tomato\Maps.Google.Com\edgelist_name.txt','r')
p=f.readlines()
f.close()

f=open(r'C:\Users\Jayant\Desktop\Tomato\Maps.Google.Com\edgelist_val.txt','r')
l=f.readlines()
f.close()

for i,j in zip(l,p):
    u,v,w=map(str,i.strip().split())
    loc1,loc2,w=map(str,j.strip().split(' | '))
    loc1='('+loc1.split('(')[1]
    loc2='('+loc2.split('(')[1]
    l11,l12=map(float,loc1[1:-1].split(','))
    l21,l22=map(float,loc2[1:-1].split(','))
    if not G.has_node(u):
        G.add_node(u,pos=(l11,l12))
    if not G.has_node(v):
        G.add_node(v,pos=(l21,l22))

for i in l:
    u,v,w=map(str,i.strip().split())
    G.add_edge(u,v,weight=int(w))

pos = nx.get_node_attributes(G,'pos')
nx.draw(G,pos)
plt.show()
