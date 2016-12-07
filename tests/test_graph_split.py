# -*- coding: utf-8 -*-

from .context import graph2
from collections import OrderedDict

import json
import unittest

snt = "0 只有 _ _ c _ 2 ADV _ _ _ * 1 不断 _ _ d _ 2 ADV _ _ _ * 2 练习 _ _ v _ -1 HED _ _ _ * 3 ， _ _ wp _ 2 WP _ _ _ * 4 才 _ _ c _ 6 ADV _ _ _ * 5 能 _ _ v _ 6 ADV _ _ _ * 6 说 _ _ v _ 2 COO _ _ _ * 7 好 _ _ v _ 6 CMP _ _ _ * 8 汉语 _ _ nz _ 7 VOB _ _ _ * 9 。 _ _ wp _ 2 WP _ _ _"
pat = "0 只有 _ _ c _ 20 ADV _ _ _ * 20 练习 _ _ v _ -1 HED _ _ _ * 40 才 _ _ c _ 60 ADV _ _ _ * 60 说 _ _ v _ 20 COO _ _ _"


from pprint import pprint

class TestGraphSplit(unittest.TestCase):
    """Basic test cases."""

    def test_has_subgraph(self):
        global snt, pat
        g0 = graph2.cnll10_to_networkx(snt)
        g1 = graph2.cnll10_to_networkx(pat)
        print(g0.nodes())
        print(g1.nodes())
        assert graph2.has_sub_graph(g0,g1)

    def test_best_mapping(self):
        g0 = graph2.cnll10_to_networkx(snt)
        g1 = graph2.cnll10_to_networkx(pat)
        bestMapping = graph2.best_mapping(g0,g1)
        ref = {0: 0, 2: 20, 4: 40, -1: -1, 6: 60}
        print(bestMapping)
        assert bestMapping == ref

    def test_split_graph(self):
        g0 = graph2.cnll10_to_networkx(snt)
        g1 = graph2.cnll10_to_networkx(pat)
        rlt = graph2.split_by_subgraph(g0, g1)
        assert len(rlt) == 2

    def test_graph_expand(self):
        g0 = graph2.cnll10_to_networkx(snt)
        patterns = [pat]
        dg = graph2.DecisionGraph2(g=g0)
        rlt = dg.expand_by_decomposition(patterns)
        pprint(dg.nodes)
        assert rlt == 1


if __name__ == '__main__':
    unittest.main()