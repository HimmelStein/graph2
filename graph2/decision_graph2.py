
from collections import defaultdict


class DecisionGraph2(object):
    """
    a decision of graph of graphs
    """
    def __init__(self, g=None):
        """
        g is an instance of networkx graph
        :param g:
        """

        self.nodes = defaultdict(lambda: {'address': None,
                                          'graph': None,
                                          'gtype': None,
                                          'head': None,
                                          'deps': defaultdict(list),
                                          'rel': None,
                                          })

        self.nodes[0].update(
            {
                'address': 0,
                'graph': g,
                'gtype': 'new' # new| complex|simple
            })

        self.root = None

    def make_node(self):
        """
        make an empty node
        :return:
        """



    def has_node_type(self, gtype=''):
        """
        check whether there is a node with gtype
        :param gtype: new| complex|simple
        :return: boolean
        """
        assert gtype in ['new'', complex', 'simple']
        for node in self.nodes:
            if node['gtype'] == gtype:
                return True
        return False

    def get_node_address_of_type(self, gtype=''):
        """
        get all address of nodes with gtype
        :param gtype: new| complex|simple
        :return: a list of node address or []
        """
        rlt = []
        if self.has_node_type(gtype=gtype):
            for node in self.nodes:
                if node['gtype'] == gtype:
                    rlt.append(node['address'])
        return rlt

    def get_all_graph_patterns(self, type=''):
        """
        get all graph patterns, type = cgraph, pgraph
        :param type:
        :return:
        """
        return []

    def expand_by_decomposition(self, patterns):
        """
        expand each node with 'gtype' = 'new'
        while there is a node with type 'new':
            for each node with type is new:
                for each pattern:
                    if node['graph'] has pattern:
                        node['gtype'] = 'complex'
                        create child node pattern, label 'cgraph'
                        childrenNodes = decompose node['graph'] with pattern
                        for i in range(len(childrenNodes):
                            childnode=childrenNodes[i]
                            create childnode for pattern node, label i
                            childnode type is 'new'

        :param patterns: a list of sub-graph patterns
        :return:
        """
        while self.has_node_type(gtype='new'):
            for address in self.get_node_address_of_type(gtype='new'):
                for pat in self.get_all_graph_patterns(type='cgraph'):
                    #if has_pattern(self.get_node_by_address(address), pat):
                    #    pass
                    pass




