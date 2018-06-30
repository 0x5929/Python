#!/usr/bin/python

"""

    NODE/MINER SERVER
    THIS SCRIPT SHOULD BE DEPLOYED TO ALL 
    NODES ACROSS THE NETWORK

        INSTALLATION/USAGE INSTRUCTIONS:
            1. HAVE SERVER SCRIPT RUNNING
            2. ADD A KNOWN HOST:PORT BY CALLING /add_peer GET api
            3. SYNC NODES BY CALLING /sync_nodes GET api
            4. SYNC BLOCKS BY CALLING /sync_blocks GET api
            5. SYNC TRANSACTIONS BY CALLING /sync_trans GET api
            6. POST ANY TRANSACTIONS BY CALLING /submit_transactions POST api
            7. MINE BY CALLING /mine GET api


"""
##################################################################################################################################################

# SERVER : 
# one node = one miner = one computer = one host machine on the mambacoin network


# sample transactions from each data of a block: (JSON object)
#{
#    "timestamp": str(datetime.datetime.now())
#    "from": "asdf-random-public-key-asdfasdf"
#    "to": "asdfas-random-public-key-asdfasdf"
#    "amount": 1
#
#}

##################################################################################################################################################

# importing required modules
from flask import Flask                                                 # for our http server
from flask import request                                               # for http server's request module
from resources import Block                                             # for blockchain class operations
from resources import Helper                                            # for helper class operations
import json                                                             # for json loading and dumping
import datetime as date                                                 # for time operations
import requests                                                         # for http request operations

##################################################################################################################################################

class Server:

#==================================================== CLASS VARIABLES ===========================================================================

    node = Flask(__name__)                          # telling flask this file name will be the name of where our web server lives
    
    this_node_transactions = []                     # initalize list of transactions for this node
    blockchain             = []                     # initialize list of blockchains for this node
    peer_nodes             = []                     # initialize list of peer nodes on this node
    
    helper       = Helper()                         # initialize our helpers
    node_helper  = helper.Node_helper()
    block_helper = helper.Blockchain_helper()
    trans_helper = helper.Transaction_helper()

    miner_address = "asdfasd-random-miner-address-1233123412asdfl3k4j"          # setting a random public address

#=================================================== INSTANCE METHODS ============================================================================

    
# transaction related handlers and methods

    def _check_trans(self, transaction):
        """
            This is an internal private api called by
            this node's submit_transaction_handler method
        
        """

        for t in Server.this_node_transactions:                     # iterating through current list of transactions 
            if json.loads(transaction) == json.loads(t):            # if input new trans is the same as any of our list, return false
                return False

        return True                                                 # if not, return true

#-------------------------------------------------------------------------------------------------------------------------------------------------

    def submit_transaction_handler(self):
        """
            This is an external api called by
            any client to post transcations
            
            Also this is an internal api called by
            peer nodes whenever a transaction is posted there
        
        """

        if request.method == 'POST':                                                    # make sure we are only handling post requests
            new_trans = request.get_json()                                              # extracting the transaction data    
            
            if self._check_trans(new_trans):                                            # making sure our transactions are actually new
                for peer in Server.peer_nodes:
                    requests.post("http://{}/submit_transaction", json=new_trans)       # broadcast to other nodes
            
                Server.this_node_transactions.append(new_trans)                         # adding new transactions to our node's list
    
                # standard output our transaction
                print "=================================================="
                print "**New Transaction**"
                print "From: {}".format(new_trans['from'])
                print "To: {}".format(new_trans['to'])
                print "Amount: {}".format(new_trans['amount'])                          # usage of format instead of formatters like %s in C
    
                return "Transaction submission successful\n"                            # response to client

#-------------------------------------------------------------------------------------------------------------------------------------------------

    def clear_trans_handler(self):
        """
            This is an internal api called by
            peer  node's mining functionality to clear 
            this node's transactions after a block is mined with all transactions
        
        """

        if request.method == 'DELETE':
            Server.this_node_transactions[:] = Server.trans_helper.ensure()     # clears transaction, this is called by miners of other nodes 
                                                                                # either we get an empty trans list or remaining unsynced trans
                                                                                # if there are any
        return ""                                                               # NOTE: ensure method will ensure all transactions are either
                                                                                # accounted and cleared/deleted, or have the remaining 
                                                                                # unaccounted transactions

#-------------------------------------------------------------------------------------------------------------------------------------------------

    def sync_trans_handler(self):                                               # called by any client to sync current node's transactions 
        """
            This is an external api called by 
            any client to sync this node's transactions with others
        
        """

        Server.this_node_transactions[:] = Server.trans_helper.consensus(Server.this_node_transactions, Server.peer_nodes)

        return "[+] Transactions synced: {}".format(str(Server.this_node_transactions))

#-------------------------------------------------------------------------------------------------------------------------------------------------

    def get_trans_handler(self):                            
        """
            This is an internal api called by
            peer nodes to extract this node's 
            transactions for syncing purposes
        
        """

        return json.dumps(Server.this_node_transactions)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # block related handlers and methods

    def sync_blocks_handler(self):  
        """
            This is an external api called by 
            any client to sync this node's block
        
        """
        
        Server.blockchain[:] = Server.block_helper.consensus(Server.blockchain, Server.peer_nodes)
        
        return "[+] Blocks synced: {}".format(str(Server.blockchain))

#-------------------------------------------------------------------------------------------------------------------------------------------------

    def get_blocks_handler(self):  
        """
            This is an internal api called by 
            peer nodes to extract this node's 
            blockchain list for syncing purposes
        
        """

        blocks = []
        
        for block in Server.blockchain:                                         # remeber our block is in block object format
            blocks.append({
                    "index"    : str(block.index),
                    "timestamp": str(block.timestamp),
                    "data"     : str(block.data),                               # data is also in json format
                    "hash"     : block.hash
                })


        return json.dumps(blocks)                                               # so we need to return json format through the server

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # peer nodes related handlers and methods

    def sync_nodes_handler(self):   
        """
            This is an external api called by 
            any clients to sync this node's 
            peer node list
        
        """

        Server.peer_nodes[:] = Server.node_helper.consensus(Server.peer_nodes)

        return "[+] Nodes synced: {}".format(str(Server.peer_nodes))

#-------------------------------------------------------------------------------------------------------------------------------------------------

    def get_nodes_handler(self):
        """
            This is an interal api called by
            peer nodes to extract this node's 
            peer nodes list for syncing purposes
        
        """
        nodes = []

        for n in Server.peer_nodes:                                 # converting into json object to be sent via http requests
            host = n.split(':')[0]
            port = n.split(':')[1]
            node = {
                "host": str(host),
                "port": str(port)
            }
            
            nodes.append(node)

        return json.dumps(nodes)                                    # after syncing everyting, convert synced nodes to json and send to client

#------------------------------------------------------------------------------------------------------------------------------------------------

    def add_peer_handler(self):
        """
            This is an external api called by
            any client to add a host node onto this 
            particular node's peer node list
        
        """
        host = request.args['host'] if 'host' in request.args else 'localhost'  # args is a dict of key value pairs of the url query, after ?
        port = request.args['port']                                             # url format: http://192.168.1.249:5000/?host=192.168.1.10&port=50
        peer = host + ':' + port
        Server.peer_nodes.append(peer)
        
        output = '[+] peer added: {}'.format(peer)
        
        print output                                                            # output to server

        return output                                                           # response to client

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # mining handler and method

    def mine_handler(self):

        # before mining, sync nodes, blocks, and transactions
        Server.peer_nodes = Server.node_helper.consensus(Server.peer_nodes)             
        Server.blockchain = Server.block_helper.consensus(Server.blockchain, Server.peer_nodes)   
        Server.this_node_transactions = Server.trans_helper.consensus(Server.this_node_transactions, Server.peer_nodes) 

        last_block = Server.blockchain[len(Server.blockchain) - 1]                      # start mining
        last_proof = last_block.data['proof-of-work']
        proof = Server.helper.proof_of_work(last_proof)                                 # grabbing proof of work

        miner_transaction = {                                                           # adding miner transactions
                "timestamp": str(datetime.datetime.now())
                "from"     : "network",
                "to"       : Server.miner_address
                "amount"   : 1
            }

        Server.this_node_transactions.append(miner_transaction)                         

        data = {
                "proof-of-work": proof,
                "transactions: " list(Server.this_node_transactions)
            }


        for peer in Server.peer_nodes:                                                  # empty transactions 
            requests.delete("http://{}/clear_trans".format(peer))                       # clear_trans api will also check for any unaccounted
                                                                                        # transactions in other node's so they are not deleted
        Server.this_node_transactions[:] = []                                           # clear this node's transactions 
        
                                                                                        # resyncing to account for any slight discrepancies 
                                                                                        # that may happen between last sync and mining procedure
        Server.peer_nodes = Server.node_helper.consensus(Server.peer_nodes)             # resync peer_nodes, and blocks
        Server.blockchain = Server.block_helper.consensus(Server.blockchain, Server.peer_nodes)              

        block = Block(last_block.index + 1, date.datetime.now(), data, last_block.hash) # creating block
                
        Server.blockchain.append(block)                                                 # finally adding block to chain

        return json.dumps({                                                             # response to client
                "index": index,
                "timestamp": str(timestamp),
                "data": data, 
                "hash": block.hash
            }) + "\n"
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    # server initializing/setup routing code
    #NOTE: we could also add another level of abstraction for node/block/transaction handlers as the project gets more complex
    # would be initialized and passed in from script execution

    def start(self):
    
        # using flask's routing decorator
        # the function will return the response for the appropriate url routing
        # and handle this url routing appropriatly
    
        # once this is called, it will use the same data and post to all nodes
        @Server.node.route('/submit_transaction', methods=['POST'])
        self.submit_transaction_handler 
    
        # once this is called, it will call /get_transactions to retrieve all transactions from peers and consensus the best one to be updated
        @Server.node.route('/sync_trans', methods=['GET'])
        self.sync_trans_handler

        # this is called by /sync_trans api 
        @Server.node.route('/get_trans', methods=['GET'])
        self.get_trans_handler
    
        # once this is called, it will call /get_blocks to retreive all blocks from all peers and consensus the best one to be updated
        @Server.node.route('/sync_blocks', methods=['GET'])
        self.sync_blocks_handler

        # this is called by /sync_blocks rest api
        @Server.node.route('/get_blocks', methods=['GET'])
        self.blocks_handler
    
        # once this is called it will call /get_nodes to retrieve all nodes from peers and consensus the best one to be updated
        @Server.node.route('/sync_nodes', methods=['GET'])
        self.sync_nodes_handler

        # this is called by /sync_nodes
        @Server.node.route('/get_nodes', methods=['GET'])
        self.nodes_handler

        # once this is called it will add a host and port to this server's nodes list
        @Server.node.route('/add_peer', methods=['GET'])
        self.add_peer_handler
    
        # once this is called it will mine a coin using proof of work, and clear transactions of this server
        # and call /clear_trans to all other nodes to clear other transactions as well
        # NOTE: all transactions are broadcasted to all nodes. 
        @Server.node.route('/mine', methods=['GET'])
        self.mine_handler
        
        # this is called by /mine api to clear all transactions across network
        @Server.node.route('/clear_trans', methods=['DELETE'])
        self.clear_trans_handler

        # making sure our webserver will be running, standard port is 5000
        Server.node.run()
    
##################################################################################################################################################

# script execution

if __name__ == "__main__":
    server = Server()               # initializing server
    server.start()                  # starting server
