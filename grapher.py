import networkx as nx
from matplotlib import pyplot as plt
G = nx.read_pajek('weighted_hero_network.txt')

def get_network(arg):
    plt.clf()
    arg = arg.upper()
    N = G.neighbors(arg)
    N.append(arg)
    H = G.subgraph(N)
    d = nx.degree(H)
    nx.draw_circular(H,with_labels=True,alpha=0.5,edge_color='0.5',
        nodelist=d.keys(), node_size=[v * 5 for v in d.values()])
    plt.show()
    plt.savefig("network.pdf")
    plt.clf()
