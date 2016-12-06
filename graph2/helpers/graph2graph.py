import networkx
from collections import OrderedDict
from nltk.parse import DependencyGraph
from networkx.algorithms.isomorphism.isomorphvf2 import DiGraphMatcher


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
    nx_nodelist = list(range(min(g.nodes.keys()),max(g.nodes.keys())))
    nxg.add_nodes_from(nx_nodelist)
    for i in nx_nodelist:
        nxg.node[i].update(g.nodes[i])
    nx_edge_list = [(n, g._hd(n), {'rel': g._rel(n)}) for n in nx_nodelist if g._hd(n)]
    nxg.add_edges_from(nx_edge_list)
    return nxg


def cnll10_to_networkx(cnnl10):
    return nltk_to_networkx(cnll10_to_nltk(cnnl10))


def has_sub_graph(g0,g1):
    gm = DiGraphMatcher(g0, g1)
    return gm.subgraph_is_isomorphic()


def all_mappings(g0, g1):
    gm = DiGraphMatcher(g0, g1)
    mappings = []
    if has_sub_graph(g0,g1):
        for _ in gm.subgraph_isomorphisms_iter():
            mappings.append(_)
    return mappings


def scoring_this_mapping(g0,g1,thisMapping, features=['word', 'tag']):
    """

    :param g0:
    :param g1:
    :param thisMapping:
    :return:
    """
    num = 0
    for id0, id1 in thisMapping.items():
        for f in features:
            if g0.node[id0].get(f, 0) == g1.node[id1].get(f, 1):
                num += 1
    return num


def scoring_mappings(g0, g1, features=['word', 'tag']):
    """

    :param g0:
    :param g1:
    :return:
    """
    scoreDic= OrderedDict()
    for thisMapping in all_mappings(g0, g1):
        thisScore = scoring_this_mapping(g0,g1,thisMapping, features=features)
        scoreDic[thisScore] = thisMapping
    return scoreDic


def best_mapping(g0, g1, features=['word', 'tag']):
    """

    :param g0:
    :param g1:
    :param features:
    :return:
    """
    scoredMappings = scoring_mappings(g0,g1, features=features)
    key = max(scoredMappings.keys())
    return scoredMappings[key]





