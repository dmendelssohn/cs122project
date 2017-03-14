import pandas as pd
ls
cd Desktop
df = pd.read_csv("hero-network.csv")
df.head()
len(df)
df = pd.read_csv("hero-network.csv",headers=False)
df = pd.read_csv("hero-network.csv",header=False)
df.head()
df = pd.read_csv("hero-network.csv",header=None)
df.head()
tall = pd.concat([df[0],df[1]])
len(tall)
len(set(tall))
l = list(set(tall))
d = {}
i = 0
for name in l:
    i+=1
    d[name] = i
d
len(l)
l[-1]
d['RAX']
df.apply(lambda row: (d[row[0]],d[row[1]]))
df.apply(lambda row: (d[row[0]],d[row[1]]),axis=1)
df.ix[0]
d["LITTLE, ABNER"]
d["PRINCESS ZANDA"]
len(df)
edges = pd.concat(df.apply(lambda row: d[row[0]],axis=1),df.apply(lambda row: d[row[1]],axis=1),axis=1)
df.apply(lambda row: d[row[0]],axis=1)
df.apply(lambda row: d[row[1]],axis=1)
left = df.apply(lambda row: d[row[0]],axis=1)
right = df.apply(lambda row: d[row[1]],axis=1)
left
right
edges = pd.concat([left,right])
namedf = data.frame(l)
namedf = Data.Frame(l)
namedf = pd.Data_Frame(l)
namedf = pd.Data.Frame(l)
namedf = pd.DataFrame(l)
namedf.head()
d["STYX II"]
namenum = namedf.apply(lambda row: d[row[0]],axis=1)
namenum.head()
verts = pd.concat([namenum,namedf])
len(verts)
verts = pd.concat([namenum,namedf],axis=1)
len(verts)
len(edges)
len(edges)/2
edges.head()
len(left)
left.head()
edges = pd.concat([left,right],axis=1)
len(edges)
edges.head()
pd.DataFrame(["*Vertices",len(verts)])
pd.DataFrame(["*Vertices",len(verts)],axis=1)
pd.DataFrame([["*Vertices"],[len(verts)]])
pd.DataFrame({0:"*Vertices",1:len(verts)})
pd.DataFrame({0:"*Vertices",1:len(verts)},index=[0,1])
pd.DataFrame({0:"*Vertices",1:len(verts)},index=[0])
verthead = pd.DataFrame({0:"*Vertices",1:len(verts)},index=[0])
edgehead = pd.DataFrame({0:"*arcs",1:len(edges)},index=[0])
edgehead
final = pd.concat([verthead,verts,edgehead,edges])
edgehead
verts.head()
verts.columns = [0,1]
verts
verts.head()
edges.head()
final = pd.concat([verthead,verts,edgehead,edges])
final.head()
final.to_csv(r'final.txt', header=None, index=None, sep=' ', mode='a')
import networkx as nx
nx.read_pajek('final.txt')
verts.head()
test = verts.apply(lambda row: str(row[1]))
test.head()
test = verts.apply(lambda row: str(row[1]),axis=1)
test.head()
test.to_csv("test.txt")
%history
test.to_csv("test.txt",sep=' ')
import csv
test.to_csv("test.txt",sep=' ',quoting=csv.QUOTE_NONNUMERIC)
csv.QUOTE_NONNUMERIC
?to_csv
pd.to_csv?
?pd.to_csv
?pd.to_csv()
pd.to_csv()
pd.to_csv
pd.to_csv?
pandas.to_csv
test.to_csv("test.txt",sep=' ', quoting=csv.QUOTE_NONNUMERIC)
import pandas as pd
test.to_csv("test.txt",sep=' ', quoting=csv.QUOTE_NONNUMERIC)
def quote(string):
    if string[0] != '"':
        string = '"' + string
    if string[-1] != '"':
        string += '"'
    return string
test.head()
test[0]
test.apply(lambda row: quote(row[0]))
test.apply(lambda row: quote(row[0]),axis=1)
test.apply(lambda row: quote(row[0]))
test.head()
test.apply(lambda row: quote(row))
verts
%history
final = pd.concat([verthead,test,edgehead,edges])
final.head()
edgehead.head()
edges.head()
verthead.head()
test.head()
vleft.head()
namenum.head()
namedf.head()
verts = pd.concat([namenum,test],axis=1)
verts.head()
test.head()
namedf = test.apply(lambda row: quote(row))
verts = pd.concat([namenum,namedf],axis=1)
verts.head()
d["STYX II"]
final = pd.concat([verthead,verts,edgehead,edges])
final.head()
final.to_csv(r'final.txt', header=None, index=None, sep=' ', mode='a')
final.to_csv(r'final.txt', header=None, index=None, sep=' ')
test
verts = pd.concat([namenum,test],axis=1)
verts.head()
final = pd.concat([verthead,verts,edgehead,edges])
final.head()
final.to_csv(r'final.txt', header=None, index=None, sep=' ')
final.to_csv(r'final.txt', header=None, index=None, sep=' ',mode='a')
final.to_csv(r'final.txt', header=None, index=None, sep=' ',mode='wb')
final.to_csv(r'final.txt', header=None, index=None, sep=' ',mode='r')
final.to_csv(r'final.txt', header=None, index=None, sep=' ',mode='w')
namedf.head()
verts = pd.concat([namenum,namedf],axis=1)
final = pd.concat([verthead,verts,edgehead,edges])
final.head()
final.to_csv(r'final.txt', header=None, index=None, sep=' ')
final.to_csv(r'final.txt', header=None, index=None, sep=' ',mode="a")
g = nx.read_pajek('final.txt')
g.neighbors('"""STYX II"""')
g.neighbors('""STYX II""')
g.neighbors('STYX II')
g.neighbors('SPIDER-MAN/PETER PAR')
len(g.neighbors('SPIDER-MAN/PETER PAR'))
g = nx.read_pajek('final.txt')
n = g.neighbors('SPIDER-MAN/PETER PAR')
len(n)
h = g.subgraph(n)
h.draw_networkx
h.draw
import matplotlib
h.draw
h
h.draw()
nx.draw(h)
nx.draw_networkx(h)
g.neighbors("STYX II")
n = g.neighbors("STYX II")
h = g.subgraph(n)
nx.draw(h)
plt.show()
matplotlib.show()
from matplotlib import pyplot as plt
plt.show()
plt.clf()
nx.draw(h)
plt.show()
n1 = g.neighbors('SPIDER-MAN/PETER PAR')
n1 = g.neighbors('SPIDER-MAN/PETER PAR')
h1 = g.subgraph(n1)
plt.clf()
nx.draw_networkx(h1)
plt.show()