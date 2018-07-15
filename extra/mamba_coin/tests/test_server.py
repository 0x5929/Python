#!/usr/bin/python


"""
    Tests for server.py

"""

import unittest
import path_helper
import datetime
import json
from mock import patch
from server import Server
from resources.block import Block
from test_compare import Test_compare

class Testcases_server(unittest.TestCase):

    def setUp(self):
        self.peer_nodes = ["192.168.1.86:5000", "192.168.1.87:5000"]

    def tearDown(self):
        pass

    def test_updateList(self):
        # test data
        host1 = "192.168.1.86:5000"
        host2 = "192.168.1.87:5000"

        trans1 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "asdf-random-public-key-asdf",
                    "to": "qwer-random-public-key-qwer",
                    "amount": 1
                }
        trans2 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "zxcv-random-public-key-zxcv",
                    "to": "hjkl-random-public-key-hjkl",
                    "amount": 3
                }

        genesis_block = Block.create_genesis_block()
        block2 = Block.create_next_block(genesis_block)

        # test 1, ensure transaction
        with patch("server.Server.this_node_transactions", []) as mock_tnt, \
             patch("server.Server.trans_helper.ensure", return_value=[trans1, trans2]):
            
            Server._updateList(ensure_transactions=True, delete_data=None)
            self.assertEqual(mock_tnt, [trans1, trans2])

        # test 2, sync this node's transactions
        with patch("server.Server.this_node_transactions", []) as mock_tnt, \
             patch("server.Server.trans_helper.consensus", return_value=[trans1, trans2]):
            
            Server._updateList(node_transactions=True)
            self.assertEqual(mock_tnt, [trans1, trans2])

        # test 3, add transactions
        with patch("server.Server.this_node_transactions", []) as mock_tnt:
            
            Server._updateList(add_trans=True, trans=trans1)
            self.assertEqual(mock_tnt, [trans1])
        
        # test 4, sync this node's blockchain
        with patch("server.Server.blockchain", []) as mock_bc, \
             patch("server.Server.block_helper.consensus", return_value=[genesis_block, block2]):
            
            Server._updateList(blockchain=True)
            self.assertEqual(mock_bc, [genesis_block, block2])

        # test 5, sync this node's peer_nodes
        with patch("server.Server.peer_nodes", []) as mock_pn, \
             patch("server.Server.node_helper.consensus", return_value=[host1, host2]):
            
            Server._updateList(peer_nodes=True)
            self.assertEqual(mock_pn, [host1, host2])

        # test 6, sync this node's peer_nodes
        with patch("server.Server.peer_nodes", []) as mock_pn:
            
            Server._updateList(add_peer=True, peer=host1)
            self.assertEqual(mock_pn, [host1])
        pass

    def test_checkTrans(self):
        # test trasactions
        trans1 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "asdf-random-public-key-asdf",
                    "to": "qwer-random-public-key-qwer",
                    "amount": 1
                }
        trans2 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "zxcv-random-public-key-zxcv",
                    "to": "hjkl-random-public-key-hjkl",
                    "amount": 3
                }
        trans3 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "uiop-random-public-key-uiop",
                    "to": "ghty-random-public-key-ghty",
                    "amount": 1
                }
        trans4 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "tygh-random-public-key-tygh",
                    "to": "bngh-random-public-key-bngh",
                    "amount": 1
                }

        
        
        my_node_trans = [trans1, trans2, trans3]
        new_trans = trans4


        # test with context
        with patch("server.Server.this_node_transactions", my_node_trans) as mock_my_node_trans:
            
            # test method call
            boo1_true = Server._check_trans(new_trans)
            boo2_false = Server._check_trans(trans3)


            self.assertTrue(boo1_true)
            self.assertFalse(boo2_false)

    def test_submitTransactionHandler(self):
        # test transactions
        trans1 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "asdf-random-public-key-asdf",
                    "to": "qwer-random-public-key-qwer",
                    "amount": 1
                }
        trans2 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "zxcv-random-public-key-zxcv",
                    "to": "hjkl-random-public-key-hjkl",
                    "amount": 3
                }
        trans3 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "uiop-random-public-key-uiop",
                    "to": "ghty-random-public-key-ghty",
                    "amount": 1
                }
        trans4 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "tygh-random-public-key-tygh",
                    "to": "bngh-random-public-key-bngh",
                    "amount": 1
                }

        # test data
        mock_request_method = "POST"
        mock_json_ret = json.dumps(trans4)
        mock_this_node_trans =  [trans1, trans2, trans3]
        expected_test_ret = [trans1, trans2, trans3, trans4]

        #tests
        with patch("server.Server.peer_nodes", self.peer_nodes) as mock_peer_nodes, patch("server.request") as mock_request:
            mock_request.method = mock_request_method
            mock_request.get_json.return_value = mock_json_ret

            # test 
            with patch.object(Server, "_check_trans", return_value=True) as mock_check_trans_True, \
                 patch("server.Server.this_node_transactions", mock_this_node_trans) as mock_tnt:
                Server.submit_transaction_handler()
                self.assertEqual(mock_tnt, expected_test_ret)

            # test2
            with patch.object(Server, "_check_trans", return_value=False) as mock_check_trans_False, \
                 patch("server.Server.this_node_transactions", []) as mock_tnt:
                Server.submit_transaction_handler()
                self.assertEqual(mock_tnt, [])
            

    def test_clearTransHandler(self):
        # test data
        trans1 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "asdf-random-public-key-asdf",
                    "to": "qwer-random-public-key-qwer",
                    "amount": 1
                }
        trans2 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "zxcv-random-public-key-zxcv",
                    "to": "hjkl-random-public-key-hjkl",
                    "amount": 3
                }
        trans3 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "uiop-random-public-key-uiop",
                    "to": "ghty-random-public-key-ghty",
                    "amount": 1
                }
        mock_request_method = "POST"
        expected_test_ret = [trans1]

        with patch("server.request") as mock_request:
            with patch("server.Server.this_node_transactions", [trans1, trans2, trans3]) as mock_this_node_transactions:
                mock_request.method = mock_request_method
                mock_request.get_json.return_value = json.dumps([trans2, trans3])         # to be deleted list of trans
                
                # test method call
                Server.clear_trans_handler()

                self.assertEqual(mock_this_node_transactions, expected_test_ret)

    def test_syncTransHandler(self):
        # test data
        trans1 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "asdf-random-public-key-asdf",
                    "to": "qwer-random-public-key-qwer",
                    "amount": 1
                }
        trans2 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "zxcv-random-public-key-zxcv",
                    "to": "hjkl-random-public-key-hjkl",
                    "amount": 3
                }
        mock_transhelper_consensus_ret = [trans1, trans2]

        with patch("server.Server.this_node_transactions", []) as mock_tnt, \
             patch("server.Server.trans_helper.consensus", return_value=mock_transhelper_consensus_ret):

            # test method call
            Server.sync_trans_handler()

            self.assertEqual(mock_tnt, mock_transhelper_consensus_ret)

    def test_getTransHandler(self):
        # test data
        trans1 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "asdf-random-public-key-asdf",
                    "to": "qwer-random-public-key-qwer",
                    "amount": 1
                }
        trans2 = {
                    "timestamp": str(datetime.datetime.now()),
                    "from": "zxcv-random-public-key-zxcv",
                    "to": "hjkl-random-public-key-hjkl",
                    "amount": 3
                }

        mock_node_trans = [trans1, trans2]

        with patch("server.Server.this_node_transactions", mock_node_trans) as mock_nt:
            
            # test method call
            test_ret = Server.get_trans_handler()

            self.assertEqual(json.dumps(mock_nt), test_ret)

    def test_syncBlocksHandler(self):
        # test data
        genesis_block = Block.create_genesis_block()
        second_block = Block.create_next_block(genesis_block)
        third_block = Block.create_next_block(second_block)

        mock_blockchain = [genesis_block, second_block, third_block]

        with patch("server.Server.block_helper.consensus", return_value=mock_blockchain), \
             patch("server.Server.blockchain", []) as mock_bc:

            # test method call
            Server.sync_blocks_handler()

            self.assertEqual(mock_bc, mock_blockchain)

    def test_getBlocksHandler(self):
        # test data
        genesis_block = Block.create_genesis_block()
        
        genesis_block_dict = {
                    "index": genesis_block.index,
                    "timestamp": genesis_block.timestamp,
                    "data": genesis_block.data,
                    "hash": genesis_block.hash
                }

        mock_blockchain = [genesis_block]
        
        expected_result = json.dumps([genesis_block_dict])

        with patch("server.Server.blockchain", mock_blockchain):

            # test method call
            test_call_ret = Server.get_blocks_handler
            
            # comp_list_of_nodes will also work here
            self.assertEqual(json.loads(test_call_ret()), json.loads(expected_result))
            

    def test_syncNodesHandler(self):
        # test data
        host1 = "192.168.1.86:5000"
        host2 = "192.168.1.87:5000"

        mock_node_consensus_ret = [host1, host2]
        with patch("server.Server.peer_nodes", []) as mock_pn, \
             patch("server.Server.node_helper.consensus", return_value=mock_node_consensus_ret):

            # test method call
            Server.sync_nodes_handler()

            self.assertEqual(mock_pn, mock_node_consensus_ret)


    def test_getNodesHandler(self):
        # test data
        host1 = "192.168.1.86:5000"
        host2 = "192.168.1.87:5000"
        
        host1_dict = {
                    "host": "192.168.1.86",
                    "port": "5000"
                }
        host2_dict = {
                    "host": "192.168.1.87",
                    "port": "5000"
                }

        mock_peer_nodes = [host1, host2]
        expected_result = json.dumps([host1_dict, host2_dict])

        with patch("server.Server.peer_nodes", mock_peer_nodes):

            # test method call
            test_ret = Server.get_nodes_handler()

            self.assertEqual(test_ret, expected_result)


    def test_addPeerHandler(self):
        # test data
        host1 = "192.168.1.86:5000"
        host2 = "192.168.1.87:5000"

        mock_get_request_args_87 = {
                            "host": "192.168.1.87",
                            "port": "5000"
                        }

        mock_get_request_args_lh = {
                            "port": "5000"
                        }

        expected_result_87 = [host1, host2]
        expected_result_lh = [host1, "localhost:5000"]

    
        with patch("server.request") as mock_request:
            with patch("server.Server.peer_nodes", [host1]) as mock_peer_nodes:
                mock_request.method = "GET"
                
                # first test
                mock_request.args = mock_get_request_args_87
                Server.add_peer_handler()

                self.assertEqual(mock_peer_nodes, expected_result_87)

            with patch("server.Server.peer_nodes", [host1]) as mock_peer_nodes:
                #second test
                mock_request.args = mock_get_request_args_lh

                Server.add_peer_handler()

                self.assertEqual(mock_peer_nodes, expected_result_lh)


    def test_mineHandler(self):
        with patch("server.datetime") as mock_server_datetime,  \
             patch("resources.block.datetime") as mock_datetime, \
             patch("server.requests") as mock_requests:
            mock_requests.post.return_value = 1
            mock_datetime.datetime.now.return_value = 'NOW'
            mock_server_datetime.datetime.now.return_value = 'NOW'

        # test data
           # mock_server.miner_address = Server.miner_address

            host1 = "192.168.1.86:5000"
            host2 = "192.168.1.87:5000"

            trans1 = {
                        "timestamp": str(mock_server_datetime.datetime.now()),
                        "from": "asdf-random-public-key-asdf",
                        "to": "qwer-random-public-key-qwer",
                        "amount": 1
                    }
            trans2 = {
                        "timestamp": str(mock_server_datetime.datetime.now()),
                        "from": "zxcv-random-public-key-zxcv",
                        "to": "hjkl-random-public-key-hjkl",
                        "amount": 3
                    }


            data = {
                    "proof-of-work": 18,
                    "transactions": list([trans1, trans2])
                }


            genesis_block = Block.create_genesis_block()
            second_block = Block.create_next_block(genesis_block)
            third_block = Block(second_block.index + 1, mock_server_datetime.datetime.now(), data, prev_hash=second_block.hash)

            mine_trans = {
                        "timestamp": str(mock_server_datetime.datetime.now()),
                        "from": "network",
                        "to": Server.miner_address,
                        "amount": 1
                    }

            mined_data = {
                    "proof-of-work": 36, 
                    "transactions": list([trans1, trans2, mine_trans])    
                }
            
            mined_block = Block(third_block.index + 1, mock_server_datetime.datetime.now(), mined_data, prev_hash=third_block.hash)
            
            expected_output = json.dumps({
                    "index": mined_block.index,
                    "timestamp": str(mined_block.timestamp),
                    "data": mined_block.data,
                    "hash": str(mined_block.hash)
                })
            
            with patch("server.Server.node_helper.consensus", return_value=[host1, host2]), \
                 patch("server.Server.block_helper.consensus", return_value=[genesis_block, second_block, third_block]), \
                 patch("server.Server.trans_helper.consensus", return_value=[trans1, trans2]), \
                 patch("server.Server.helper.proof_of_work", return_value=36), \
                 patch("server.Server.this_node_transactions", data["transactions"]) as mock_tnt, \
                 patch("server.Server.blockchain", []) as mock_bc, \
                 patch("server.Server.peer_nodes", []) as mock_pn:

                # test method call
                test_ret = Server.mine_handler()

                # test for node transactions (method sideeffect)
                # this tests the second sync function, usually will result in []
                # but this time mock sync returns [trans1, trans2]
                self.assertEqual(mock_tnt, [trans1, trans2])

                # test for block mined (method output)
                boo = Test_compare.comp_block_dict(json.loads(test_ret), json.loads(expected_output))
                self.assertTrue(boo)
                
                # test for blockchain congruency (network effect)
                # NOTE: mined_block is not added here because of the second sync of mine method, and it is resuing the block consensus return
                boo = Test_compare.comp_list_of_block_obj(mock_bc, [genesis_block, second_block, third_block])
                self.assertTrue(boo)

            # below is to test if the current chain is empty, genesis block must be created, and returned is the second (mined) block of chain
            with patch("server.Server.node_helper.consensus", return_value=[host1, host2]), \
                 patch("server.Server.block_helper.consensus", return_value=[]), \
                 patch("server.Server.trans_helper.consensus", return_value=[trans1, trans2]), \
                 patch("server.Server.helper.proof_of_work", return_value=36), \
                 patch("server.Server.this_node_transactions", data["transactions"]) as mock_tnt, \
                 patch("server.Server.blockchain", []) as mock_bc, \
                 patch("server.Server.peer_nodes", []) as mock_pn:
                mine_trans = {
                        "timestamp": str(mock_server_datetime.datetime.now()),
                        "from": "network",
                        "to": Server.miner_address,
                        "amount": 1
                    }

                mined_data = {
                    "proof-of-work": 36, 
                    "transactions": list([trans1, trans2, mine_trans])    
                }
            
                mined_block = Block(genesis_block.index + 1, mock_server_datetime.datetime.now(), mined_data, prev_hash=genesis_block.hash)
            
                expected_output = json.dumps({
                    "index": mined_block.index,
                    "timestamp": str(mined_block.timestamp),
                    "data": mined_block.data,
                    "hash": str(mined_block.hash)
                })

                # test method call
                test_ret = Server.mine_handler()


                # test for block mined (method output)
                boo = Test_compare.comp_block_dict(json.loads(test_ret), json.loads(expected_output))
                self.assertTrue(boo)
                
if __name__ == "__main__":
    unittest.main()


