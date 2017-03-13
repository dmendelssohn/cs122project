import networkx as nx
from matplotlib import pyplot as plt
import os 
G = nx.read_pajek('weighted_hero_network.txt')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_color(arg,name):
    if name == arg:
        return 'g'
    else:
        return 'r'

def get_network(arg,conn_num=False):
    limit = False
    plt.clf()
    arg = arg.upper()
    if arg not in G.nodes():
        return (0,0,0,0)
    else:
        N = G.neighbors(arg)
        N.append(arg)
        H = G.subgraph(N)
        d = nx.degree(H)
        weights = H[arg]

        most_apps = sorted([(x,weights[x][0]['weight']) for x in weights], key=lambda i: i[1],reverse=True)
        highest = most_apps[0][1]
        i = 0
        for j in most_apps:
            if j[1] == highest:
                i +=1
        most = [x[0].title() for x in most_apps[:i]]

        weights[arg] = {0:{'weight':highest}}

        if conn_num and conn_num < len(N):
            limit = True
            lim_N = [x[0] for x in most_apps[:conn_num-1]] + [arg]
            lim_H = G.subgraph(lim_N)
            lim_d = nx.degree(lim_H)
            nx.draw_circular(lim_H,with_labels=True,alpha=0.5,edge_color='0.5',
                nodelist=lim_d.keys(), node_size=[weights[v][0]['weight'] * 5 for v in lim_d.keys()],
                node_color=[get_color(arg,v) for v in lim_d.keys()])
            plt.savefig(os.path.join(BASE_DIR,'ui/static/lim_network.jpg'))
            plt.clf()

        nx.draw_circular(H,with_labels=True,alpha=0.5,edge_color='0.5',
            nodelist=d.keys(), node_size=[weights[v][0]['weight'] * 5 for v in d.keys()],
            node_color=[get_color(arg,v) for v in d.keys()])
        plt.savefig(os.path.join(BASE_DIR,'ui/static/network.jpg'))
        plt.clf()
        return (1,most,len(N),limit)
