#!/usr/bin/python

import unittest
from mock import patch
from a import A

class Testt(unittest.TestCase):
    def test_my_method(self):
        with patch("a.A.my_list", [1,2,3]):
            A.my_method(4)
            self.assertEqual(A.my_list, [1,2,3,4])
                    
if __name__ == "__main__" :
    unittest.main()
