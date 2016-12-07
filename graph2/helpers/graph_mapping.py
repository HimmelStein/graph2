from collections import OrderedDict
from networkx.algorithms.isomorphism.isomorphvf2 import DiGraphMatcher


def has_sub_graph(g0,g1):
    gm = DiGraphMatcher(g0, g1)
    return gm.subgraph_is_isomorphic()

def get_all_graph_patterns(type='cgraph'):
    """
    get all graph patterns of type
    :param type:
    :return: a list of nx graphs
    """
    pass

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


def top_n_mapping(g0, g1, n=1, features=['word', 'tag']):
    """
    :param g0:
    :param g1:
    :param features:
    :return:
    """
    scoredMappings = scoring_mappings(g0,g1, features=features)
    keyLst = list(scoredMappings.keys())
    keyLst.sort(reverse=True)
    topNLst = keyLst[:n]
    return [scoredMappings[key] for key in topNLst]

