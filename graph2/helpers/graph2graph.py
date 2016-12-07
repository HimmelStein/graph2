import networkx
from nltk.parse import DependencyGraph


def is_last_node_empty(g):
    """
    g is an instance of DependencyGraph
    :param g:
    :return: boolean
    """
    n = max(g.nodes.keys())
    if g.nodes[n]['address'] == None and g.nodes[n]['word'] == None:
        return True
    else:
        return False


def remove_last_node(g):
    """
    g is an instance of DependencyGraph
    :param g:
    remove last key-value of g
    :param g:
    :return:
    """
    n = max(g.nodes.keys())
    g.nodes.pop(n)
    return g


def cnll10_to_nltk(cnll10):
    """
    load cnll10 string to nltk dependent parser
    :param cnll10:
    :return:
    """
    cnll10 = cnll10.replace('*','\n').replace('_ _ _', '_ _') +'\n'
    g = DependencyGraph(cnll10)
    # if is_last_node_empty(g):
    #     remove_last_node(g)
    return g


def nltk_to_networkx(g):
    """
    transform a nltk DependencyGraph instance into networkx instance
    :param g:
    :return: an instance of DiGraph in networkx
    """
    nxg = networkx.DiGraph()
    nx_nodelist = list(g.nodes.keys())
    nx_nodelist.sort()
    nxg.add_nodes_from(nx_nodelist)
    for i in nx_nodelist:
        nxg.node[i].update(g.nodes[i])
    nx_edge_list = [(g._hd(n), n, {'rel': g._rel(n)}) for n in nx_nodelist if g._hd(n)]
    nxg.add_edges_from(nx_edge_list)
    return nxg


def cnll10_to_networkx(cnnl10):
    return nltk_to_networkx(cnll10_to_nltk(cnnl10))







