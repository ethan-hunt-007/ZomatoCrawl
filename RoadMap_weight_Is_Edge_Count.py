import networkx as nx
import googlemaps
import csv
import matplotlib.pyplot as plt
import math as mt
import time

def main():
    global my_loc,gmaps,R,keys,zones
    #zones={"shyambazar metro station":(22.601343,88.372822),"dum dum metro station":(22.621250,88.392888),"salt lake nicco park":(22.571143,88.421805)}
    zones=[(22.534667,88.337770),(22.583298,88.351593),(22.596139,88.451369),(22.499317,88.370983),(22.629245,88.385053),(22.651829,88.427262),(22.593104,88.470083),(22.587207, 88.374325)]
    keys=['AIzaSyAMdDIbyp5N8MqwvVvmqwsD4-vgUoLqSRg','AIzaSyBNiTP5dvW_2FS_vSr89oU0Q8Wc-lhzfjs','AIzaSyCjTjiBfYyUzHQDr8-PIO5KF3XvVu6wNjo','AIzaSyCJPRL3K_w3l_DtoM0Xhpv2KrKVWlQfuAo','AIzaSyDcBHi3Cs0n4QsSOhl6K5fiRkKV9gif2h4','AIzaSyDpbFkJanVQNsUekdg3Josx_3j226Pkgqo','AIzaSyB1l0hL8-YM2A1FCeZIJfb8nQY2hlgn51I','AIzaSyBH4OukzwdQKOQD_PK9ZtGRqqx9twsVdm0']
    R=6373
    '''from_res = input("Enter the starting restaurant:-")
    to_res = input("Enter upto how many restaurant u wan't to see:-")'''
    path = "C:\Users\Jayant\Desktop\Tomato\Tomato_db_sorted.csv"
    #My Location : 22.587212, 88.374389
    #gmaps = googlemaps.Client(key='AIzaSyAMdDIbyp5N8MqwvVvmqwsD4-vgUoLqSRg')
    my_loc = (22.587212, 88.374389)
    res_loc,xy = get_loc(path)
    G=nx.Graph()
    for zone,num in zip(zones,xrange(len(zones))):
        print "Fetching graph of Zone_%d"%num
        gmaps = googlemaps.Client(key=keys[num])
        G.add_node("Zone_%d_%s"%(num,str(zone)),pos=zone)
        c=1
        res=1
        node_hash = {}
        for loc in xy:
            print res
            try:
                location = get_directions(zone,loc)
            except:
                print loc
            nodes = [["Zone_%d_%s"%(num,str(zone)),zone]]
            for locs in location[1:-1]:
                node = str(locs)
                '''node = get_address(locs)
                if c not in nodes:
                    G.add_node(c,pos=locs)
                nodes.append(c)
                c=c+1'''
                if not G.has_node(node):
                    G.add_node(node,pos=locs)
                nodes.append([node,locs])
            G.add_node("Res#%d%s"%(res,loc),pos=loc)
            nodes.append(["Res#%d%s"%(res,loc),loc])
            res+=1
            for i in xrange(1,len(nodes)):
                if G.has_edge(nodes[i-1][0],nodes[i][0]):
                    wt=G[nodes[i-1][0]][nodes[i][0]]['weight']
                else:
                    wt=0
                G.add_edge(nodes[i-1][0],nodes[i][0],weight=wt+1)
                #G.add_edge(nodes[i-1][0],nodes[i][0],weight=findDistance(nodes[i-1][1][0],nodes[i][1][0],nodes[i-1][1][1],nodes[i][1][1]))
    pos = nx.get_node_attributes(G,'pos')
    #print pos
    nx.draw(G,pos)
    plt.show()
    #print_edge(G)
    save_edgelist(G)

def get_loc(path):
    res_loc = {}
    xy = []
    with open(path,"r") as c:
        f=csv.reader(c)
        for row in f:
            if row[0]!='Restaurant':
                x,y=float(row[6]),float(row[7])
                xy.append((x,y))
                res_loc[(x,y)]=row[0]
    return res_loc,xy

def get_address(loc):
    geo = gmaps.reverse_geocode(loc)
    return str(geo[0]['formatted_address'])

def get_directions(my_loc,loc):
    directions = gmaps.directions(my_loc,loc,mode='walking')
    if len(directions)==0:
        directions = gmaps.directions(my_loc,loc)
    latlon = []
    for steps in directions[0]['legs'][0]['steps']:
        latlon.append(steps['start_location'])
    latlon.append(directions[0]['legs'][0]['steps'][-1]['end_location'])
    location = []
    for loc in latlon:
        location.append((loc['lat'],loc['lng']))
    return location
    '''for i in xrange(1,len(latlon)):
        n1_x=latlon[i]['lat']
        n1_y=latlon[i]['lng']
        n2_x=latlon[i-1]['lat']
        n2_y=latlon[i-1]['lon']
        (n1_x,n1_y)=LatLon_to_xy(n1_x,n1_y)
        (n2_x,n2_y)=LatLon_to_xy(n2_x,n2_y)'''


def print_edge(G):
    for edge in G.edges_iter():
        print edge[0],edge[1],G[edge[0]][edge[1]]['weight']


def save_edgelist(G):
    hash_for = {}
    c=1
    res=1
    for edge in G.edges_iter():
        if 'Zone' in edge[0]:
            ed=edge[0].split('_')
            hash_for[edge[0]]='Zone'+ed[1]
        if 'Zone' in edge[1]:
            ed=edge[1].split('_')
            hash_for[edge[1]]='Zone'+ed[1]
        if 'Res#' in edge[0]:
            hash_for[edge[0]]="R#%d"%res
            res+=1
        if 'Res#' in edge[1]:
            hash_for[edge[1]]="R#%d"%res
            res+=1
        try:
            key=hash_for[edge[0]]
        except:
            hash_for[edge[0]]=c
            c+=1
        try:
            key=hash_for[edge[1]]
        except:
            hash_for[edge[1]]=c
            c+=1
    f=open("hash_file.txt","w")
    for i,j in hash_for.iteritems():
        print >>f,i,j
    f.close()
    f=open("edgelist_val.txt","w")
    for edge in G.edges_iter():
        print >>f,hash_for[edge[0]],hash_for[edge[1]],G[edge[0]][edge[1]]['weight']
    f.close()
    f=open("edgelist_name.txt","w")
    for edge in G.edges_iter():
        print >>f,edge[0],'|',edge[1],'|',G[edge[0]][edge[1]]['weight']
    f.close()


def findDistance(lat1,lat2,lon1,lon2):
    lat1=deg2grad(lat1)
    lat2=deg2grad(lat2)
    lon1=deg2grad(lon1)
    lon2=deg2grad(lon2)

    dlat=lat2-lat1
    dlon=lon2-lon1

    a  = mt.pow(mt.sin(dlat/2),2) + mt.cos(lat1) * mt.cos(lat2) * mt.pow(mt.sin(dlon/2),2)
    c  = 2 * mt.atan2(mt.sqrt(a),mt.sqrt(1-a))
    dk = c * R
    km=roundi(dk)
    return km

def deg2grad(deg):
    rad=deg*mt.pi/180
    return rad

def roundi(x):
    return round(x*1000)/1000
        
if __name__=='__main__':
    main()
