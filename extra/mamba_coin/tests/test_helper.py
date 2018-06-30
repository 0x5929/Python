#!/usr/bin/python


"""
    Tests for helper.py

"""

import unittest
import path_helper
from resources.helper import Helper.Node_helper as nodehelper
from resources.helper import Helper.Blockchain_helper as blockhelper
from resources.helper import Helper.Transaction_helper as transhelper


class Testcases_helper(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_node_resolveHost(self):
        pass
    
    def test_node_consensus(self):
        pass

    def test_node_findOtherNodes(self):
        pass

    def test_node_updateNodes(self):
        pass

    def test_block_consensus(self):
        pass

    def test_block_findOtherChains(self):
        pass

    def test_block_updateBlockchain(self):
        pass

    def test_trans_consensus(self):
        pass

    def test_trans_findOtherTrans(self):
        pass

    def test_trans_updateTransactions(self):
        pass

    def test_trans_ensure(self):
        pass

    def test_trans_compareTrans(self):
        pass



if __name__ == "__main__":
    unittest.main()



