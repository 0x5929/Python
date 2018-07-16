#!/usr/bin/python


#   This project is an idea inspired by the following blog: 
#   can be found at https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b
#   I have renamed the coin into mamba coin, b/c kobe rules
#   but all credit still goes to the original author of the blogpost
        

# importing modules we need
import hashlib
import datetime

# let us create the structure of each block
class Block:
    """
        superClass: None
        handler class that is responsible for creating a block
    
    """
    initialized_data = {
                "proof-of-work": None,
                "transactions": None
                }


    @classmethod
    def create_genesis_block(cls):
        """
            param1 obj: cls object
            return obj: Block class genesis block object

            external api called by block_helper.create_gen_block
        
        """

        return cls(0, datetime.datetime.now(), cls.initialized_data, prev_hash="0")            # return genesis block
    
    #NOTE: this method is only used for testing purposes, and creating dummy next blocks
    #      the node server will never implement this method, but rather create a Block instance with the correct data/transactions when mining
    #      should probably hide it with _
    @classmethod
    def create_next_block(cls, last_block):
        """
            param1 obj: cls object
            param2 obj: last block object 

            return obj: Block class object

            external api used in creating test blocks
        
        """
        this_index = last_block.index + 1                                                       # collecting info for next block creation
        this_timestamp = datetime.datetime.now()
        this_data = cls.initialized_data
        this_prevHash = last_block.hash

        return cls(this_index, this_timestamp, this_data, prev_hash=this_prevHash)              # return the next block

    def __init__(self, index, timestamp, data, prev_hash=None, current_hash=None):
        """
            param1 obj: self object
            param2 int: index of block
            param3 str: timestamp of block
            param4 dict: data of block {[trans]}
            param5 str: previous hash if creating new block, defaults to None
            param6 str: current hash if creating an existed block

            return obj: Block class object
        
        
        """
        self.index = int(index)                 # enforce/convert to integer format
        self.timestamp = str(timestamp)         # enforce/convert to string format
        self.data = dict(data)                  # enforce dictionary format
        self.prev_hash = prev_hash
        self.current_hash = current_hash
        
        # added feature
        if current_hash is not None:            # if current_hash is passed in
            self.hash = current_hash            # we use the current hash
        else:
            self.hash = self._hash_me()         # else, create a new one 

    def _hash_me(self):
        """
            param1 obj: self object
            return str: hash

            internal api called by Block.__init__ to return a new hash 
        
        """
        sha = hashlib.sha256()                  # creating our hash object

        sha.update(str(self.index) +            # updating the hash object of concatenated string of all the data in the block 
                   str(self.timestamp) +        # this will be then hashed together and spit out by the hexdigest method
                   str(self.data) +
                   str(self.prev_hash))                            

        return sha.hexdigest()

    def __getitem__(self, key):                 # so we can access block['attr']
            return getattr(self, key)



