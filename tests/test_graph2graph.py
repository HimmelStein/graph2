# -*- coding: utf-8 -*-

from .context import graph2
from collections import OrderedDict

import json
import unittest

chCNLL10 = "0 他 _ _ r _ 1 SBV _ _ _ * 1 导演 _ _ v _ -1 HED _ _ _ * 2 了 _ _ u _ 1 RAD _ _ _ * 3 那场 _ _ r _ 4 ATT _ _ _ * 4 话剧 _ _ n _ 1 VOB _ _ _ * 5 。 _ _ wp _ 1 WP _ _ _"
deCNLL10 = "1 Er er PRO PPER 3|Sg|Masc|Nom 2 subj _ _  * 2 hat haben V VAFIN 3|Sg|Pres|Ind 0 root _ _  * 3 bei bei PREP APPR Dat 2 pp _ _  * 4 jenem jene ART PDAT _|Dat|Sg 5 det _ _  * 5 Theater Theater N NN Fem|Dat|Sg 3 pn _ _  * 6 Regie Regie N NN Fem|Dat|Sg 5 app _ _  * 7 geführt führen V VVPP _ 2 aux _ _  * 8 . . $. $. _ 0 root _ _  *  * "



class TestGraph2Graph(unittest.TestCase):
    """Basic test cases."""


    def test_cnll10_to_nltk(self):
        global chCNLL10, deCNLL10
        chGraph = graph2.cnll10_to_nltk(chCNLL10)
        deGraph = graph2.cnll10_to_nltk(deCNLL10)
        print(chGraph.nodes)
        print(deGraph.nodes)
        assert chGraph.nodes[1]['word'] == '导演'
        assert deGraph.nodes[7]['word'] == 'geführt'

    def test_scoring_mappings(self):
        global chCNLL10, deCNLL10
        g0 = graph2.cnll10_to_networkx(chCNLL10)
        scoredMappings = graph2.scoring_mappings(g0,g0)
        ref = [OrderedDict([(12, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, -1: -1}), (8, {0: 2, 1: 1, 2: 0, 3: 3, 4: 4, -1: -1})]),
               OrderedDict([(14, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, -1: -1}),
                            (10, {0: 5, 1: 1, 2: 2, 3: 3, 4: 4, 5: 0, -1: -1}),
                            (8, {0: 2, 1: 1, 2: 5, 3: 3, 4: 4, 5: 0, -1: -1})])
               ]
        print(scoredMappings)
        assert scoredMappings in ref

    def test_best__mapping(self):
        global chCNLL10, deCNLL10
        g0 = graph2.cnll10_to_networkx(chCNLL10)
        bestMapping = graph2.best_mapping(g0,g0)
        ref =[{0: 0, 1: 1, 2: 2, 3: 3, 4: 4, -1: -1},
              {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, -1: -1}
              ]
        print(bestMapping)
        assert bestMapping in ref


if __name__ == '__main__':
    unittest.main()