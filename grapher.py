import networkx as nx
from matplotlib import pyplot as plt
G = nx.read_pajek('clean_hero_network.txt')

def get_network(arg):
    plt.clf()
    arg = arg.upper()
    N = G.neighbors(arg)
    N.append(arg)
    H = G.subgraph(N)
    nx.draw_circular(H,with_labels=True,alpha=0.2,edge_color='0.75')
    plt.show()
    plt.savefig("network.pdf")
    plt.clf()