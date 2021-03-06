import pandas as pd
import csv
import re
import networkx as nx

def clean(string):
    '''
    Reformats a single string to work with networkx
    Inputs:
      string: (str) line in network csv to be cleaned
    Outputs network line with proper formatting
    '''
    string = string.strip()
    singlename = re.findall(r'^[^/]+',string)[0]
    fullname = re.findall(r'^([^,]+)(?:[\,][ ])*([^|]*)[|]*[ ]*(.*)',singlename)[0]
    if len(fullname[1]) > 0:
        name = fullname[1].strip() + ' ' + fullname[0].strip() + ' ' + fullname[2].strip()
    else:
        name = fullname[0].strip() + ' ' + fullname[2].strip()
    name = name.replace('|','')
    nameclean = ' '.join(name.split())
    return "'" + '"' + nameclean + '"' + "'"

dfraw = pd.read_csv("hero-network.csv",header=None)
leftname = dfraw[0].apply(lambda row: clean(row))
rightname = dfraw[1].apply(lambda row: clean(row))
df = pd.concat([leftname,rightname],axis=1)
tall = pd.concat([df[0],df[1]])
l = pd.DataFrame(list(set(tall)))
d = {}
i = 0
for name in l[0]:
    i+=1
    d[name] = i
leftnum = df.apply(lambda row: d[row[0]],axis=1)
rightnum = df.apply(lambda row: d[row[1]],axis=1)
namedf = pd.DataFrame(l)
namenum = namedf.apply(lambda row: d[row[0]],axis=1)
verts = pd.concat([namenum,namedf],axis=1)
edges = pd.concat([leftnum,rightnum],axis=1)
verthead = pd.DataFrame({0:"*Vertices",1:len(verts)},index=[0])
edgehead = pd.DataFrame({0:"*arcs",1:len(edges)},index=[0])
verts.columns = [0,1]
final = pd.concat([verthead,verts,edgehead,edges])
final = final.reset_index(drop=True)
final.to_csv(r'clean_hero_network.txt', header=None, index=None, sep=' ')

M = nx.read_pajek("clean_hero_network.txt")
G = nx.Graph()
for u,v,data in M.edges_iter(data=True):
    w = data['weight'] if 'weight' in data else 1.0
    if G.has_edge(u,v):
        G[u][v]['weight'] += w
    else:
        G.add_edge(u, v, weight=w)

nx.write_pajek(G,"weighted_hero_network.txt")