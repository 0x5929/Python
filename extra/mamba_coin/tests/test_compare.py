#!/usr/bin/python


# this is a helper for our testing package, to compare two dicts, lists, and Block objects

# import dependencies
import path_helper
from resources.block import Block

class Test_compare:

    @classmethod
    def comp_list_of_block_obj(cls, first, second):
        if (type(first) == list) and (type(second) == list):
            for obj in first:
                if not isinstance(obj, Block):
                    print "list of obj in first param is not list of block, fatal"
            for s_obj in second:
                if not isinstance(s_obj, Block):
                    print "list of obj in second param is not list of blocks, fatal"

            return cls(first, second)._is_same_list_of_blocks()

        print "compare list of objects received one or more none list type in params, fatal"

    @classmethod
    def comp_list_of_block_dict(cls, first, second):
        if (type(first) == list) and (type(second) == list):
            for obj in first:
                if not isinstance(obj, dict):
                    print "list of obj in first param is not list of block dicts, fatal"
            for s_obj in second:
                if not isinstance(s_obj, dict):
                    print "list of obj in second param is not list of blocks dicts, fatal"

            return cls(first, second)._is_same_list_of_block_dict()

        print "compare list of dicts received one or more none list type in params, fatal"

    @classmethod
    def comp_block_dict(cls, first, second):
        if (type(first) == dict) and (type(second) == dict):

            return cls(first, second)._is_same_block_dict()

        print "compare block dicts received one or more none dict type in params, fatal"

    @classmethod
    def comp_list_of_nodes(cls, first, second):
        if (type(first) == list) and (type(second) == list):
            for s1 in first:
                if not isinstance(s1, str):
                    print "list of nodes in the first param is not a list of string hosts, fatal"
            for s2 in second:
                if not isinstance(s2, str):
                    print "list of nodes in the second param is not a list of string hosts, fatal"

            return cls(first,second)._is_same_list_of_nodes()
        else:
            print "compare list of nodes received one or more is not list type in params, fatal"

    @classmethod
    def comp_list_of_trans_dict(cls, first, second):
        if (type(first) == list) and (type(second) == list):
            for s1 in first:
                if not isinstance(s1, dict):
                    print "list of transaction dict in the first param is not a list of dict, fatal"
            for s2 in second:
                if not isinstance(s2, dict):
                    print "list of transaction dict in the second param is not a list of dict, fatal"

            return cls(first, second)._is_same_list_of_trans()
                    
        else:
            print "compare list of transaction dicts received one or more is not list type in params, fatal"


    def __init__(self, first, second):
        self.first = first
        self.second = second

    def _is_same_list_of_blocks(self):
        if len(self.first) != len(self.second):
            return False

        for first_obj in self.first:
            if first_obj.index != self.second[self.first.index(first_obj)].index:
                print "index problem"
                return False
            elif first_obj.timestamp != self.second[self.first.index(first_obj)].timestamp:
                print "timestamp problem"
                return False
            elif first_obj.data != self.second[self.first.index(first_obj)].data:
                print "data problem"
                return False
            elif first_obj.hash != self.second[self.first.index(first_obj)].hash:
                print "hash problem"
                return False
        return True
    
    def _is_same_list_of_block_dict(self):
        if len(self.first) != len(self.second):
            print "two list have different lengths"
            return False
        
        for block in self.first:
            if block['index'] != self.second[self.first.index(block)]['index']:
                print "index problem"
                return False
            elif block['timestamp'] != self.second[self.first.index(block)]['timestamp']:
                print "timestamp problem"
                return False
            if block['data'] != self.second[self.first.index(block)]['data']:
                print "data problem"
                return False
            if block['hash'] != self.second[self.first.index(block)]['hash']:
                print "hash problem"
                return False
        return True

    def _is_same_block_dict(self):
        
        for key in self.first.keys():
            if self.first[key] != self.second[key]: 
                # the only reason why they diff, its because of the dic within a dict might have different order of keys
                if (type(self.first[key]) == dict) and (type(self.second[key]) == dict):
                    for k in self.first[key].keys():
                        if self.first[key][k] != self.second[key][k]:
                            return False
                else:
                    print "something is wrong"
                    return False

        return True
            

    def _is_same_list_of_nodes(self):
        if len(self.first) != len(self.second):
            print "two lists have different lengths"
            return False

        for h1 in self.first:
            if h1 not in self.second:
                print "which did not match: ", h1
                return False

        # if we have not returned false yet, return true
        return True

    # same as _is_same_list_of_nodes
    def _is_same_list_of_trans(self):
        if len(self.first) != len(self.second):
            return False
        for h1 in self.first:
            if h1 not in self.second:
                print "returning false"
                print h1
                return False

        return True
