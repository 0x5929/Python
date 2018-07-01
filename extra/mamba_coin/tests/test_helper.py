#!/usr/bin/python


"""
    Tests for helper.py

"""

import unittest
import path_helper
from mock import patch
from resources.helper import Helper.Node_helper as nodehelper
from resources.helper import Helper.Blockchain_helper as blockhelper
from resources.helper import Helper.Transaction_helper as transhelper


class Testcases_helper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.node_helper = nodehelper()
        cls.block_helper = blockhelper()
        cls.trans_helper = transhelper()
        cls.peer_nodes = ['192.168.1.87:5000', '192.168.1.86:5000']

    @classmethod
    def tearDownClass(cls):
        pass

    def test_node_resolveHost(self):
        self.assertEqual(Testcases_helper.node_helper._resolve_host(), "192.168.1.249")
    
    def test_node_consensus(self):
        # if i am node C
        nodeA_addr = '192.168.1.86:5000'
        nodeB_addr = '192.168.1.87:5000'
        nodeC_addr = '192.168.1.249:5000'
        nodeA_nodes = [nodeB_addr]
        nodeB_nodes = [nodeA_addr, nodeC_addr]
        find_other_nodes_ret = [nodeA_nodes, nodeB_nodes]
        
        with patch('nodehelper._find_other_nodes') as mock_method:
            mock_method.return_value = find_other_nodes_ret
            
            mock_ret = [nodeA_addr, nodeB_addr] 
            self.assertEqual(Testcases_helper.node_helper.consensus(), mock_ret)



    def test_node_findOtherNodes(self):
        with patch('nodehelper.requests.get') as mock_get:
            all_nodes_on_each_network = Testcases_helper.node_helper._find_other_nodes(Testcases_helper.peer_nodes) 
            

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



