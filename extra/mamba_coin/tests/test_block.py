#!/usr/bin/python


"""
    Tests for block.py

"""

import unittest
import path_helper
import hashlib
import datetime
from test_compare import Test_compare
from resources.block import Block


class Testcases_block(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_createGenesisBlock(self):
        # test class method call
        genesis_block = Block.create_genesis_block()
        
        # expected result
        data = {
                "proof-of-work": None,
                "transactions": None
                }
        expected_result = Block(0, genesis_block.timestamp, data, prev_hash="0")

        # test
        expected_true = Test_compare.comp_list_of_block_obj([genesis_block], [expected_result])
        self.assertTrue(expected_true)

    def test_createNextBlock(self):
        # test data
        genesis_block = Block.create_genesis_block()

        # test class method call
        next_block = Block.create_next_block(genesis_block)

        # expected result
        data = {
                "proof-of-work": None,
                "transactions": None
                }
        expected_result = Block(1, next_block.timestamp, data, prev_hash=genesis_block.hash)

        # test
        expected_true = Test_compare.comp_list_of_block_obj([next_block], [expected_result])
        self.assertTrue(expected_true)

    def test_hashMe(self):
        # test data
        genesis_block = Block.create_genesis_block()

        # test instance method call
        hash_me_test_result = genesis_block.hash

        # expected result
        sha = hashlib.sha256()

        sha.update("0" + 
                str(genesis_block.timestamp) + 
                str(genesis_block.data) + 
                "0")
        expected_result = sha.hexdigest()


        # test
        self.assertEqual(hash_me_test_result, expected_result)

    # this tests the block creation using constructor instead of class method
    # this will also test dict get attr of each block (could be isolated in its own tests)
    def test_Block(self):
        genesis_block = Block.create_genesis_block()
        test_time = datetime.datetime.now()
        test_data = {
                "proof-of-work": None,
                "transactions": None
                }
        test_block = Block(genesis_block.index + 1, test_time, test_data, prev_hash=genesis_block.hash)

        expected_result = Block(genesis_block.index + 1, test_time, test_data, current_hash=test_block.hash)

        boo_true = Test_compare.comp_list_of_block_obj([test_block], [expected_result])
        self.assertTrue(boo_true)

        # testing getitem
        self.assertEqual(test_block['index'], 1)
        self.assertEqual(test_block['timestamp'], str(test_time))
        self.assertEqual(test_block['data'], test_data)
        self.assertEqual(test_block['hash'], test_block.hash)



if __name__ == "__main__":
    unittest.main()



