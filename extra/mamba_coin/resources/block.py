#!/usr/bin/python


#   This project is an idea inspired by the following blog: 
#   I have renamed the coin into mamba coin, b/c kobe rules
#   but all credit still goes to the original author of the blogpost
#   blog can be found at https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b
        

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

        return cls(0, datetime.datetime.now(), cls.initialized_data, prev_hash="0")
    
    #NOTE: this method is only used for testing purposes, and creating dummy next blocks
    #      the node server will never implement this method, but rather create a Block instance with the correct data/transactions when mining
    #      should probably hide it with _
    @classmethod
    def create_next_block(cls, last_block):
        this_index = last_block.index + 1
        this_timestamp = datetime.datetime.now()
        this_data = cls.initialized_data
        this_prevHash = last_block.hash

        return cls(this_index, this_timestamp, this_data, prev_hash=this_prevHash)

    def __init__(self, index, timestamp, data, prev_hash=None, current_hash=None):
        self.index = int(index)
        self.timestamp = str(timestamp)
        self.data = dict(data)                      # improvements: need to enforce type checker
        self.prev_hash = prev_hash
        self.current_hash = current_hash
        
        # added feature
        if current_hash is not None:
            self.hash = current_hash
        else:
            self.hash = self._hash_me()

    def _hash_me(self):
        sha = hashlib.sha256()                  # creating our hash object

        sha.update(str(self.index) +            # updating the hash object of concatenated string of all the data in the block 
                   str(self.timestamp) +        # this will be then hashed together and spit out by the hexdigest method
                   str(self.data) +
                   str(self.prev_hash))                            

        return sha.hexdigest()

    def __getitem__(self, key):                # so we can access block['attr']
            return getattr(self, key)




# starting our blockchain 
#blockchain = [create_genesis_block()]
#prev_block = blockchain[0]
#
#num_of_blocks_to_add = 25
#
#for i in range(0, num_of_blocks_to_add):
#    block_to_add = create_next_block(prev_block)
#    blockchain.append(block_to_add)
#
#    prev_block = block_to_add
#
#    #stdo
#    print "================================================================================="
#    print "Block #%d has been added to the blockchain!" % block_to_add.index 
#    print "Hash: %s" % str(block_to_add.hash)
#    print "Data: %s" % str(block_to_add.data)
#    print "Time: %s" % str(block_to_add.timestamp)



