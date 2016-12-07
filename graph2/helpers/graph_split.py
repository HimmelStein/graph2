from networkx import DiGraph
import networkx as nx
from .graph_mapping import has_sub_graph
from .graph_mapping import best_mapping


def split_by_subgraph(g0, g1):
    """
    remove mapped edges fromg g0,
    remove mapped functional words from g0
    remove none node
    check number of roots (in_degree == 0)
    copy out each connected_component
    :param g0:
    :param g1:
    :return: a list of connected component sub-graph
    """
    rlt = []
    ng = g0.copy()
    assert has_sub_graph(g0,g1)
    mapping = best_mapping(g0,g1)
    inv_map = {v: k for k, v in mapping.items()}
    for nd0, nd1 in g1.edges():
        d0 = inv_map[nd0]
        d1 = inv_map[nd1]
        ng.remove_edge(d0,d1)

    for nd in mapping.keys():
        if is_node_of_functional_word(ng.node[nd]) or is_empty_node(ng.node[nd]):
            ng.remove_node(nd)

    roots = get_root(ng)
    assert len(roots)>1

    for root in roots:
        print('root', root)
        nsubg = DiGraph()
        edges = list(nx.bfs_edges(ng, root))
        print('edges', edges)
        nsubg.add_edges_from(edges)
        for d0, d1 in edges:
            nsubg[d0][d1] = ng[d0][d1]
        for nd in nsubg.nodes():
            nsubg.node[nd] = ng.node[nd]

        rlt.append(nsubg)
    return rlt


def get_root(g):
    rlt = []
    for n in g.nodes():
        if g.in_degree(n) == 0:
            rlt.append(n)
    return rlt


def is_node_of_functional_word(dict):
    """
    dict is the feature dictionary of a node
    :param dict:
    :return: boolean
    """
    if dict.get('tag', 'x') not in ['v'] \
            and dict.get('tag', 'x') in ['c'] :
        return True
    else:
        return False


def is_empty_node(dict):
    """
    dict is the feature dictionary of a node
    :param dict:
    :return: boolean
    """
    if dict.get('address', 'x') == None and dict.get('tag', 'x') == None\
            and dict.get('head', 'x') == None and dict.get('word', 'x') == None:
        return True
    else:
        return False
