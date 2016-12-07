
from collections import defaultdict
from .helpers.graph_mapping import has_sub_graph
from .helpers.graph_split import split_by_subgraph
from .helpers.graph2graph import cnll10_to_networkx


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
                'gtype': 'new' # new|complex|simple
            })

        self.root = None
        self.numOfNodes = 1

    def add_node_to(self, where, wtype='', g=None, gtype='new', rel=''):
        """
        make an empty node
        :return: an empty node, which is not append to the self.nodes
        """
        newAddress = self.numOfNodes + 1
        self.nodes[where]['deps'].update({rel:[newAddress]})
        self.nodes[where]['gtype'] = wtype
        if wtype != 'simple':
            newNode = {'address': newAddress,
                         'graph': g,
                         'gtype': gtype,
                         'head': where,
                         'deps': defaultdict(list),
                         'rel': rel,
                        }
            self.nodes[newAddress].update(newNode)
            return newAddress
        return None

    def set_gtype_of_node(self, address, gtype):
        self.nodes[address]['gtype'] = gtype

    def node_type_qual(self, gtype=''):
        """
        check whether there is a node with gtype
        :param gtype: new| complex|simple
        :return: boolean
        """
        assert gtype in ['new', 'complex', 'simple', 'cgraph']
        for address in self.nodes.keys():
            if self.nodes[address]['gtype'] == gtype:
                return True
        return False

    def nodes_of_type(self, gtype=''):
        """
        get all address of nodes with gtype
        :param gtype: new| complex|simple
        :return: a list of node address or []
        """
        rlt = []
        if self.node_type_qual(gtype=gtype):
            for address in self.nodes.keys():
                if self.nodes[address]['gtype'] == gtype:
                    rlt.append(self.nodes[address]['address'])
        return rlt

    def get_graph_by_node_address(self, address):
        return self.nodes[address]['graph']

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
        :return: number of cgraphs
        """
        numOfCGraphs = 0
        while self.node_type_qual(gtype='new'):
            for address in self.nodes_of_type(gtype='new'):
                for pat in patterns:
                    g0 = self.get_graph_by_node_address(address)
                    g1 = cnll10_to_networkx(pat)
                    if has_sub_graph(g0, g1):
                        numOfCGraphs += 1
                        components = split_by_subgraph(g0, g1)
                        newAddress=self.add_node_to(address,wtype='complex',g=g1,gtype='new',rel='SUBG')
                        for componentGraph in components:
                            self.add_node_to(newAddress,wtype='cgraph',g=componentGraph, gtype='new',rel='COMG')
                    else:
                        self.set_gtype_of_node(address, 'simple')
        return numOfCGraphs










