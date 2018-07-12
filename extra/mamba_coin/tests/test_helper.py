#!/usr/bin/python


"""
    Tests for helper.py

"""

import unittest
import path_helper
import datetime
import json
from test_compare import Test_compare
from mock import patch
from resources.helper import Helper, requests
from resources.block import Block


#NOTE: all the test data here could be encapsulated in another file, to be imported from to read from
# alot of repeating stuff here

class Test_helper(unittest.TestCase):

    # instance method
    def setUp(self):
        #NOTE: im not sure if I node/block/trans helper needs helper to be initaitiaed first?
        self.helper = Helper()
        self.node_helper = self.helper.Node_helper()
        self.block_helper = self.helper.Blockchain_helper()
        self.transhelper = self.helper.Transaction_helper()
        self.peer_nodes = ['192.168.1.87:5000', '192.168.1.86:5000']

    def tearDown(self):
        pass
        
    def test_helper_proofOfWork(self):
        self.assertEqual(self.helper.proof_of_work(None), 9)
        self.assertEqual(self.helper.proof_of_work(9), 18)

    def test_node_resolveHost(self):
        self.assertEqual(self.node_helper._resolve_host(), "192.168.1.249")
    
    def test_node_consensus(self):
        # if i am node C
        nodeA_addr = '192.168.1.86:5000'
        nodeB_addr = '192.168.1.87:5000'
        nodeC_addr = '192.168.1.249:5000'

        nodeA_addr_dict = {
                    "host": "192.168.1.86",
                    "port": "5000"
                }

        nodeB_addr_dict = {
                    "host": "192.168.1.87",
                    "port": "5000"
                }

        nodeC_addr_dict = {
                    "host": "192.168.1.249",
                    "port": "5000"
                }

        nodeA_nodes = [nodeB_addr_dict, nodeC_addr_dict]
        nodeB_nodes = [nodeA_addr_dict, nodeC_addr_dict]# added nodeB addr for testing purposes, normally the return of 
                                                                        # findothernodes is [[dict]] and dict is usually not the same
        mock_method_ret = []
        mock_method_ret.extend((nodeA_nodes, nodeB_nodes))
        
        with patch('resources.helper.Helper.Node_helper._find_other_nodes') as mock_method:
            # only mocking all the elements of findothernodes to be the same -> nodeB_nodes
            mock_method.return_value = mock_method_ret
            
            # even with only nodeB_nodes, tests should come out as our mock_Ret
            ret = [nodeA_addr, nodeB_addr] 
            
            self.assertTrue(Test_compare.comp_list_of_nodes(self.node_helper.consensus(self.peer_nodes), ret))
            
            #self.assertEqual(self.node_helper.consensus(self.peer_nodes), ret)



    def test_node_findOtherNodes(self):
        test_get_return_content = json.dumps(
                    [
                        {"host": "192.168.1.86", "port": "5000"}, 
                        {"host": "192.168.1.87", "port": "5000"}
                    ] 
                )

        all_nodes_on_each_network = [json.loads(test_get_return_content), json.loads(test_get_return_content)]
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200

            # on each get return, the content is as such
            mock_get.return_value.content = test_get_return_content
            
            self.assertEqual(self.node_helper._find_other_nodes(self.peer_nodes), all_nodes_on_each_network)

    def test_node_haveNode(self):
        node = {"host": "192.168.1.87", "port": "5000"}
        my_peer_nodes = ["192.168.1.86:5000", "192.168.1.87:5000"]

        self.assertTrue(self.node_helper._have_node(node, my_peer_nodes))
        self.assertFalse(self.node_helper._have_node(node, ["192.168.1.86:5000"]))

    # poorly written 
    def test_node_updateNodes(self):
        my_peer_nodes = ["192.168.1.86:5000", "192.168.1.87:5000"]
        to_be_added_nodes = [{"host":"192.168.1.88", "port":"5000"}]

        to_be_added_nodes2 = [{"host": "192.168.1.86", "port": "5000"}, 
                                {"host": "192.168.1.87", "port": "5000"}, 
                                { "host":"192.168.1.88", "port":"5000"}]
        

        ret_new_peer_nodes = ["192.168.1.86:5000", "192.168.1.87:5000", "192.168.1.88:5000"]

        self.assertEqual(self.node_helper._update_nodes(my_peer_nodes, to_be_added_nodes), ret_new_peer_nodes)
        self.assertEqual(self.node_helper._update_nodes([], to_be_added_nodes), ["192.168.1.88:5000"])

    def test_block_consensus(self):
        test_peer_nodes = ['192.168.1.86:5000', '192.168.1.87:5000']
        ret = []
        nodeA_chains_dict = []                                   # has two blocks   format: [{dict}]
        nodeB_chains_dict = []                                   # has three blocks
        nodeC_chains_dict = []                                   # has one block    this is the same format returned from _find_other_chains

        genesis_block = Block.create_genesis_block()
        second_block = Block.create_next_block(genesis_block)
        third_block = Block.create_next_block(second_block)

        genesis_block_dict = {
                        "index": str(genesis_block.index),
                        "timestamp": str(genesis_block.timestamp),
                        "data": genesis_block.data,
                        "hash": str(genesis_block.hash)
                }

        second_block_dict = {
                        "index": str(second_block.index),
                        "timestamp": str(second_block.timestamp),
                        "data": second_block.data,
                        "hash": str(second_block.hash)
                }

        third_block_dict = {
                        "index": str(third_block.index),
                        "timestamp": str(third_block.timestamp),
                        "data": third_block.data,
                        "hash": str(third_block.hash)
                }
        
        nodeA_chains_dict.extend((genesis_block_dict, second_block_dict))

        nodeB_chains_dict.extend((genesis_block_dict, second_block_dict, third_block_dict))

        nodeC_chains_dict.append(genesis_block_dict)

        ret.extend((nodeA_chains_dict, nodeB_chains_dict))                                      # what is returned from _find_other_chains

        ret_chain = [genesis_block, second_block, third_block]                                  # expended returned chain output from consensus

        with patch('resources.helper.Helper.Blockchain_helper._find_other_chains') as mock_find_other_chains:

            mock_find_other_chains.return_value = ret

            self.assertTrue(Test_compare.comp_list_of_block_obj( \
                    self.block_helper.consensus([genesis_block], test_peer_nodes), \
                    ret_chain))
            self.assertTrue(Test_compare.comp_list_of_block_obj( \
                    self.block_helper.consensus([genesis_block, second_block, third_block], test_peer_nodes), \
                    ret_chain))
            


    def test_block_findOtherChains(self):

        test_peer_nodes = ['192.168.1.86:5000', '192.168.1.87:5000']

        test_get_ret_chain = []                                   # has two blocks

        genesis_block = Block.create_genesis_block()

        genesis_block_dict = {
                        "index": str(genesis_block.index),
                        "timestamp": str(genesis_block.timestamp),
                        "data": str(genesis_block.data),
                        "hash": genesis_block.hash
                }

        # need to create test dictionary data of the block object
        test_get_ret_chain.append(genesis_block_dict)

        second_block = Block.create_next_block(genesis_block)

        second_block_dict = {
                        "index": str(second_block.index),
                        "timestamp": str(second_block.timestamp),
                        "data": str(second_block.data),
                        "hash": second_block.hash
                }

        test_get_ret_chain.append(second_block_dict)
        

        test_get_ret_chain = json.dumps(test_get_ret_chain)

        chains = [json.loads(test_get_ret_chain), json.loads(test_get_ret_chain)] # technically using our previous dictionaries would work



        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = test_get_ret_chain

            self.assertEqual(self.block_helper._find_other_chains(test_peer_nodes), chains)

    def test_block_updateBlockchain(self):
        nodeA_chains = []                                   # has two blocks
        nodeB_chains = []                                   # has three blocks

        genesis_block = Block.create_genesis_block()
        second_block = Block.create_next_block(genesis_block)
        third_block = Block.create_next_block(second_block)

        genesis_block_dict = {
                        "index": str(genesis_block.index),
                        "timestamp": str(genesis_block.timestamp),
                        "data": genesis_block.data,
                        "hash": str(genesis_block.hash)
                }

        second_block_dict = {
                        "index": str(second_block.index),
                        "timestamp": str(second_block.timestamp),
                        "data": second_block.data,
                        "hash": str(second_block.hash)
                }

        third_block_dict = {
                        "index": str(third_block.index),
                        "timestamp": str(third_block.timestamp),
                        "data": third_block.data,
                        "hash": str(third_block.hash)
                }

        nodeA_chains.extend((genesis_block_dict, second_block_dict))

        nodeB_chains.extend((genesis_block_dict, second_block_dict, third_block_dict))

        test_my_block = [genesis_block, second_block] 
        test_peer_block = nodeB_chains
        test2_my_block = [genesis_block, second_block, third_block]
        test2_peer_block = nodeA_chains

        ret_chain = test2_my_block                              # expected return from update_blockchain
        
        # assertion tests
        self.assertTrue(Test_compare.comp_list_of_block_obj( \
                self.block_helper._update_blockchain(test_my_block, test_peer_block), \
                ret_chain))

        self.assertTrue(Test_compare.comp_list_of_block_obj( \
                self.block_helper._update_blockchain(test2_my_block, test2_peer_block), \
                ret_chain))


    def test_trans_consensus(self):
        test_trans1 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "asdf-random-public-key-asdf", 
                "to": "zxcvzxc-random-public-key-azxcvz", 
                "amount": 2}

        test_trans2 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "wertwert-random-public-key-asdf", 
                "to": "yuioyuio-random-public-key-azxcvz", 
                "amount": 5}

        nodeA_trans = [test_trans1, test_trans2]
        nodeB_trans = [test_trans1]

        ret = [nodeA_trans, nodeB_trans]
        my_trans = nodeB_trans

        with patch("resources.helper.Helper.Transaction_helper._find_other_transactions") as mock_other_trans:
            mock_other_trans.return_value = ret
            
            #self.assertTrue(Test_compare.comp_list_of_trans_dict(self.transhelper.consensus(my_trans, self.peer_nodes), nodeA_trans))
            self.assertIs(self.transhelper.consensus(my_trans, self.peer_nodes), nodeA_trans)

    def test_trans_findOtherTrans(self):
        test_peer = ["192.168.1.86:5000", "192.168.1.87:5000"]
        test_trans1 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "asdf-random-public-key-asdf", 
                "to": "zxcvzxc-random-public-key-azxcvz", 
                "amount": 2}

        test_trans2 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "wertwert-random-public-key-asdf", 
                "to": "yuioyuio-random-public-key-azxcvz", 
                "amount": 5}

        nodeA_trans = [test_trans1, test_trans2]
        test_get_ret = json.dumps(nodeA_trans)

        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = test_get_ret

            self.assertEqual(self.transhelper._find_other_transactions(test_peer), [nodeA_trans, nodeA_trans])

    def test_trans_updateTransactions(self):
        test_trans1 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "asdf-random-public-key-asdf", 
                "to": "zxcvzxc-random-public-key-azxcvz", 
                "amount": 2}

        test_trans2 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "wertwert-random-public-key-asdf", 
                "to": "yuioyuio-random-public-key-azxcvz", 
                "amount": 5}

        nodeA_trans = [test_trans1, test_trans2]
        nodeB_trans = [test_trans1]
        
        self.assertEqual(self.transhelper._update_transactions(nodeB_trans, nodeA_trans), nodeA_trans)
        self.assertEqual(self.transhelper._update_transactions(nodeA_trans, nodeB_trans), nodeA_trans)
    
    def test_trans_ensure(self):
        test_trans1 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "asdf-random-public-key-asdf", 
                "to": "zxcvzxc-random-public-key-azxcvz", 
                "amount": 2}

        test_trans2 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "wertwert-random-public-key-asdf", 
                "to": "yuioyuio-random-public-key-azxcvz", 
                "amount": 5}

        test_trans3 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "jhkkh-random-public-key-asdf", 
                "to": "lkmzxcv-random-public-key-azxcvz", 
                "amount": 2}

        test_trans4 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "kukljh-random-public-key-asdf", 
                "to": ",mnkjhyuioyuio-random-public-key-azxcvz", 
                "amount": 5}

        nodeA_trans = [test_trans1, test_trans2, test_trans3]
        nodeB_trans = [test_trans1, test_trans2]
        nodeC_trans = [test_trans1, test_trans2, test_trans3, test_trans4]                                # my node
        nodeD_trans = [test_trans1, test_trans2, test_trans3]

        test_mock_ret = [nodeA_trans, nodeB_trans]
        with patch("resources.helper.Helper.Transaction_helper._find_other_transactions") as mock_method:
            mock_method.return_value = test_mock_ret

            self.assertEqual(self.transhelper.ensure(nodeC_trans, self.peer_nodes), [test_trans4])
            self.assertEqual(self.transhelper.ensure(nodeD_trans, self.peer_nodes), [])

    def test_trans_compareTrans(self):
        test_trans1 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "asdf-random-public-key-asdf", 
                "to": "zxcvzxc-random-public-key-azxcvz", 
                "amount": 2}

        test_trans2 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "wertwert-random-public-key-asdf", 
                "to": "yuioyuio-random-public-key-azxcvz", 
                "amount": 5}

        test_trans3 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "jhkkh-random-public-key-asdf", 
                "to": "lkmzxcv-random-public-key-azxcvz", 
                "amount": 2}

        test_trans4 = {
                "timestamp": str(datetime.datetime.now()), 
                "from": "kukljh-random-public-key-asdf", 
                "to": ",mnkjhyuioyuio-random-public-key-azxcvz", 
                "amount": 5}
        nodeC_trans = [test_trans1, test_trans2, test_trans3, test_trans4]          # this is my trans
        nodeA_trans = [test_trans1, test_trans2]                                    # this is peer trans
        
       # self.assertTrue(
       #     Test_compare.comp_list_of_trans_dict(
       #         self.transhelper._compare_trans(nodeC_trans, nodeA_trans), 
       #             [test_trans3, test_trans4]))

        self.assertEqual(self.transhelper._compare_trans(nodeC_trans, nodeA_trans), [test_trans3, test_trans4])
        self.assertEqual(self.transhelper._compare_trans(nodeA_trans, nodeA_trans), [])


if __name__ == "__main__":
    unittest.main()



