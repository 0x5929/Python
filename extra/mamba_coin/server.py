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
*           7. MINE BY CALLING /mine GET api


"""

#   This project is an idea inspired by the following blog: 
#   can be found at https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b
#   I have renamed the coin into mamba coin, b/c kobe rules
#   but all credit still goes to the original author of the blogpost



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
import sys                                                              # for system program implementation
import json                                                             # for json loading and dumping
import datetime                                                         # for time operations
import requests                                                         # for http request operations
from flask import Flask                                                 # for our http server
from flask import request                                               # for http server's request module
from resources import Helper                                            # for helper class operations

##################################################################################################################################################

class Server:
    """
        superClass: None

        class respnsible for running a server 
        at each node of the network
        interacts with Helper and Block class internally
        but also interacts with user externally
        

    """

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


#=================================================== CLASS METHODS ==============================================================================

    # note the classmethod below could be encapsulated into another server operation helper class, 
    # with each test case have a corresponding class method. 
    @classmethod
    def _updateList(cls, **kwargs):
        """
            param1 obj: cls reference object
            param2 dict: keyword argument dictionary
            return None: this method is responsible for updating all list operations
        
            This is an internal api called by every method that needed to perform
            some sort of operations on the class lists: peer_nodes, blockchain, this_node_transactions
            
        """
        if kwargs is not None and 'ensure_transactions' in kwargs and kwargs['ensure_transactions'] is True:

            cls.this_node_transactions[:] = cls.trans_helper.ensure(cls.this_node_transactions, kwargs['delete_data'])

        elif kwargs is not None and 'node_transactions' in kwargs and kwargs['node_transactions'] is True:

            cls.this_node_transactions[:] = cls.trans_helper.consensus(cls.this_node_transactions, cls.peer_nodes)
        
        elif kwargs is not None and 'add_trans' in kwargs and kwargs['add_trans'] is True:

            # future improvements:  need to have a transaction caluclator, to caluclate the validity of the transaction
            cls.this_node_transactions.append(kwargs['trans'])                                  

        elif kwargs is not None and 'blockchain' in kwargs and kwargs['blockchain'] is True:

            cls.blockchain[:] = cls.block_helper.consensus(cls.blockchain, cls.peer_nodes)

        elif kwargs is not None and 'peer_nodes' in kwargs and kwargs['peer_nodes'] is True:

            cls.peer_nodes[:] = cls.node_helper.consensus(cls.peer_nodes)

        elif kwargs is not None and 'add_peer' in kwargs and kwargs['add_peer'] is True:
            cls.peer_nodes.append(kwargs['peer'])

        else:

            pass
        
#------------------------------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def _sync_all_lists(cls, **kwargs):
        """
            param1 obj: cls object
            
            return None: syncs peer_nodes, blockchain, this_node_transactions 

            This is an internal api called by miner, and clear_trans handler
            since all transactions are broadcasted, and host node's responsible for syncing 
            peer_nodes with the network, so only changes aplied to the blockchain will need us to resync. 
        
        """
        if len(kwargs.keys()) == 0:                                         # sync all lists
            cls._updateList(peer_nodes=True)
            cls._updateList(blockchain=True)
            cls._updateList(node_transactions=True)
        elif kwargs is not None and "peer_nodes" in kwargs:                 # sync only peer_nodes
            cls._updateList(peer_nodes=True)
        elif kwargs is not None and "blockchain" in kwargs:                 # sync only blockchain
            cls._updateList(blockchain=True)
        elif kwargs is not None and "node_transactions" in kwargs:          # sync only this_node_transactions
            cls._updateList(node_transactions=True)
            

            

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# transaction related handlers and methods

    @classmethod
    def _check_trans(cls, transaction):
        """
            param1 obj: cls object
            param2 dict: a transaction dictionary to be checked

            return bool: whether or not this node's transaction list contains the transactions

            This is an internal private api called by
            this node's submit_transaction_handler method
        
        """

        for t in cls.this_node_transactions:                        # iterating through current list of transactions 
            if json.dumps(transaction) == json.dumps(t):            # if input new trans is the same as any of our list, return false
                return False

        return True                                                 # if not, return true

#-------------------------------------------------------------------------------------------------------------------------------------------------

    @classmethod
    def submit_transaction_handler(cls):
        """
            param1 obj: cls object
            return sideeffect: handler listens to POST request of /submit_transaction api
            
            This is an external api called by
            any user to post transcations
            
            Also this is an internal api called by
            peer nodes whenever a transaction is posted there
        
        """

        if request.method == 'POST':                                                    # make sure only handle post requests
            new_trans = json.loads(request.get_json())                                  # extracting the transaction data    
            
            if cls._check_trans(new_trans) is True:                                     # making sure transactions are actually new

                # added feature as per bitcoin white paper
                try:
                    for peer in cls.peer_nodes:
                        requests.post("http://{}/submit_transaction", json=new_trans)   # broadcast to other nodes
                except:
                    pass

                cls._updateList(add_trans=True, trans=new_trans)                        # adding new transactions to this node's list
                
                return "Transaction submission successful\n"                            # response through server

#-------------------------------------------------------------------------------------------------------------------------------------------------

    @classmethod
    def clear_trans_handler(cls):
        """
            param1 obj: cls object
            return sideeffect: handler listens to DELETE request of /clear_trans api

            This is an internal api called by
            peer  node's mining functionality to clear 
            this node's transactions after a block is mined with all transactions
            or have the unaccounted transactions left
        
        """

        if request.method == 'POST':                                                    
            delete_data = json.loads(request.get_json())                                # extract to be deleted data
            cls._updateList(ensure_transactions=True, delete_data=delete_data)          # delete transactions
            cls._sync_all_lists(blockchain=True)                                        # to grab the new blockchain                

        return ""                                                   

#-------------------------------------------------------------------------------------------------------------------------------------------------

    @classmethod
    def sync_trans_handler(cls):                                               
        """
            param1 obj: cls object
            return sideeffect: handler listens to GET request of /sync_trans api

            This is an external api called by 
            any user to sync this node's transactions with others
        
        """

        cls._sync_all_lists(node_transactions=True)                                     # sync this_node_transactions

        return "\n[+] Transactions synced: {}".format(str(cls.this_node_transactions))

#-------------------------------------------------------------------------------------------------------------------------------------------------

    @classmethod
    def get_trans_handler(cls):                            
        """
            param1 obj: cls object
            return sideeffect: handler listens to GET request of /sync_trans api

            This is an internal api called by
            peer nodes to extract this node's 
            transactions for syncing purposes
        
        """
        return json.dumps(cls.this_node_transactions)                                   # return json format of this node's transaction list


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # block related handlers and methods

    @classmethod
    def sync_blocks_handler(cls):  
        """
            param1 obj: cls object
            return sideeffect: handler listens to GET request of /sync_blocks api
            
            This is an external api called by 
            any user to sync this node's block
        
        """
        
        cls._sync_all_lists(blockchain=True)                                            # sync blockchain

        return "\n[+] Blocks synced: {}".format(str(cls.blockchain))

#-------------------------------------------------------------------------------------------------------------------------------------------------

    @classmethod
    def get_blocks_handler(cls):  
        """
            param1 obj: cls object
            return sideeffect: handler listens to GET request of /get_blocks api

            This is an internal api called by 
            peer nodes to extract this node's 
            blockchain list for syncing purposes
        
        """

        blocks = []
        
        for block in cls.blockchain:                                            # remember block is in block object format
            blocks.append({
                    "index"    : block.index,                                   # block.index is int 
                    "timestamp": str(block.timestamp),
                    "data"     : block.data,                                    # block.data is already in dict format
                    "hash"     : str(block.hash)
                })


        return json.dumps(blocks)                                               # return json format through the server

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # peer nodes related handlers and methods

    @classmethod
    def sync_nodes_handler(cls):   
        """
            param1 obj: cls object
            return sideeffect: handler listens to GET request of /sync_nodes api

            This is an external api called by 
            any user to sync this node's 
            peer node list
        
        """


        cls._sync_all_lists(peer_nodes=True)                                    # sync peer_nodes

        return "\n[+] Nodes synced: {}".format(str(cls.peer_nodes))             # response through server

#-------------------------------------------------------------------------------------------------------------------------------------------------

    @classmethod
    def get_nodes_handler(cls):
        """
            param1 obj: cls object
            return sideeffect: handler listens to GET request of /get_nodes api

            This is an interal api called by
            peer nodes to extract this node's 
            peer nodes list for syncing purposes
        
        """
        nodes = []

        for n in cls.peer_nodes:                                    # converting into json objects to be sent via http requests
            host = n.split(':')[0]
            port = n.split(':')[1]
            node = {
                "host": str(host),
                "port": str(port)
            }
            
            nodes.append(node)

        return json.dumps(nodes)                                    # after syncing everyting, convert synced nodes to json and send thru server 

#------------------------------------------------------------------------------------------------------------------------------------------------

    @classmethod
    def add_peer_handler(cls):
        """
            param1 obj: cls object
            return sideeffect: handler listens to GET request of /add_peer api

            This is an external api called by
            any user to add a host node onto this 
            particular node's peer node list
        
        """
        
        # args is a dict of key value pairs of the url query, after ?
        # url format: http://192.168.1.249:5000/add_peer/?host=192.168.1.10&port=50

        if request.method == "GET":
            host = request.args['host'] if 'host' in request.args else 'localhost'      # if there are no ip, we use localhost
                                                                               
            port = request.args['port']                                                 # extract data from GET query 
            peer = host + ':' + port
            
            cls._updateList(add_peer=True, peer=peer)                                   # add peer
        
        return '\n[+] peer added: {}'.format(peer)                                      # response thru server

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # mining handler and method

    @classmethod
    def mine_handler(cls):
        """
            param1 obj: cls object
            return sideeffect: handler listens to GET request of /mine api

            This is an external api called by 
            any user to mine a mamba coin 
            (Kobe's face in front, coin value in back)
            and lock in all transactions since the last mined coin, 
            add the mine coin with new proof of work with the locked in
            transactions, unto to the network blockchain list
        
        """

        # before mining, sync nodes, blocks, and transactions
        cls._sync_all_lists()

        # after the first sync, lets see if a genesis block is present
        if len(cls.blockchain) == 0:
            gen_block = cls.block_helper.create_gen_block()
            cls.blockchain.append(gen_block)                                    # if not, create genesis block to start chain for network
    
        # start mining
        last_block = cls.blockchain[len(Server.blockchain) - 1]                 # grabbing the last block 
        last_proof = last_block.data['proof-of-work']                           # grabbing the proof of work from the last block
        proof = cls.helper.proof_of_work(last_proof)                            # generating a new proof from the last one                            
        miner_transaction = {                                                   # adding miner transactions
                "timestamp": str(datetime.datetime.now()),
                "from"     : "network",
                "to"       : cls.miner_address,
                "amount"   : 1
            }

        cls.this_node_transactions.append(miner_transaction)                    # append the new transaction to the transaction list

        data = {                                                                # the data property of a mamba coin
                "proof-of-work" : proof,
                "transactions" : list(cls.this_node_transactions)
            }

        mined_block = cls.block_helper.create_block(last_block.index + 1, datetime.datetime.now(), data, last_block.hash)
        cls.blockchain.append(mined_block)                                              # adding block to chain

        # clean up
            # exclude miner transaction
        delete_data = json.dumps(cls.this_node_transactions[:(len(Server.this_node_transactions) - 1)])          

        for peer in cls.peer_nodes:                                                     # empty the accounted transactions 
            try: 
                requests.post("http://{}/clear_trans".format(peer), json=delete_data)   # clear_trans api will check for any unaccounted 
            except:                                                                     # transactions in other node's so they are not deleted
                pass
                                                                                        
        cls.this_node_transactions[:] = []                                              # clear this node's transactions 
        
                                                                                        # resyncing to account for any slight discrepancies 
                                                                                        # that may happen between last sync and mining procedure

        # resync peer_nodes, and blocks, and trans
        cls._sync_all_lists()

        return json.dumps({                                                             # response thru server
                "index": mined_block.index,
                "timestamp": str(mined_block.timestamp),
                "data": mined_block.data, 
                "hash": str(mined_block.hash)
            }) + "\n"
    

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    

    @classmethod
    def start(cls, port=None):
        """
        param1 obj: cls object
        param2 str: port number default to 5000
        return sideeffect: server initializes/setup routing code
        
        using flask's routing decorator to route, 
        the decorated function will return the response for the appropriate url routing
        and handle this url routing appropriatly

        """
        # once called, it will use the same data and post to all nodes
        @cls.node.route('/submit_transaction', methods=['POST'])
        def submit_transaction(): return cls.submit_transaction_handler() 

        # once called, it will call /get_trans to retrieve all transactions from peers and consensus the best one to be updated
        @cls.node.route('/sync_trans', methods=['GET'])
        def sync_trans(): return cls.sync_trans_handler()

        # called by /sync_trans api 
        @cls.node.route('/get_trans', methods=['GET'])
        def get_trans(): return cls.get_trans_handler()
    
        # once called, it will call /get_blocks to retreive all blocks from all peers and consensus the best one to be updated
        @cls.node.route('/sync_blocks', methods=['GET'])
        def sync_blocks(): return cls.sync_blocks_handler()

        # called by /sync_blocks rest api
        @cls.node.route('/get_blocks', methods=['GET'])
        def get_blocks(): return cls.blocks_handler()
    
        # once called it will call /get_nodes to retrieve all nodes from peers and consensus the best one to be updated
        @cls.node.route('/sync_nodes', methods=['GET'])
        def sync_nodes(): return cls.sync_nodes_handler()

        # called by /sync_nodes
        @cls.node.route('/get_nodes', methods=['GET'])
        def get_nodes(): return cls.nodes_handler()

        # once called it will add a host and port to this server's nodes list
        @cls.node.route('/add_peer', methods=['GET'])
        def add_peer(): return cls.add_peer_handler()
    
        # once called it will mine a coin using proof of work, and clear transactions of this server, 
        # call /clear_trans to all other nodes to clear/delete accounted transactions
        @cls.node.route('/mine', methods=['GET'])
        def mine(): return cls.mine_handler()
        
        # called by /mine api to clear all transactions across network
        @cls.node.route('/clear_trans', methods=['DELETE'])
        def clear_trans(): return cls.clear_trans_handler()

        # making sure webserver will be running eternally, standard port is 5000
        try:
            cls.node.run(port=port)
        except:
            print "\n[!] cls had trouble starting at port {}".format(port)
            print "[!] Exiting..."
            sys.exit(1)


#=================================================== STATIC METHODS ============================================================================


    @staticmethod
    def _usage():
        print "\n\n"
        
        print """
        
        [+] Welcome to Mambacoin network server node
        
        [+] Current time is: %s 
        [+] External program dependencies: cURL

        [+] Please execute the following commands in a different env/terminal

            $ curl "host:port/add_peer/?host=<host>&port=<port>"        ---- Add peer node to node list
            $ curl "host:port/sync_nodes"                               ---- Sync node list
            $ curl "host:port/sync_blocks"                              ---- Sync blockchain list
            $ curl "host:port/sync_trans"                               ---- Sync transaction list 
            $ curl "host:port/submit_transactions" \\                    ---- Post transactions to node
                    -H "application/json"          \\
                    -d "{"timestamp":<transaction timestamp>,\\
                         "from"     : <transaction from address>, \\
                         "to"       : <transaction to address>, \\
                         "amount"   : <transaction ammount>}"
            $ curl "host:port/mine"                                     ---- Mine mamba coin and solidify all transactions since last mine

        
        [+] This project is derived from snakecoin: https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b
        
        """ %str(datetime.datetime.now())

        print "\n\n"

    
##################################################################################################################################################

# script execution

if __name__ == "__main__":
    try:
        Server._usage()                          # displaying usage details
        if len(sys.argv) > 1:
            port = sys.argv[1] 
            Server.start(port=port)              # starting server
        else:
            Server.start()
    except KeyboardInterrupt:
        print "[!] Requested shutdown, exiting..."
        sys.exit(0)
