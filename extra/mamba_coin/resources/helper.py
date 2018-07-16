#!/usr/bin/python


# this file is a helper file that will be utilized in ../server.py

#   This project is an idea inspired by the following blog: 
#   can be found at https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b
#   I have renamed the coin into mamba coin, b/c kobe rules
#   but all credit still goes to the original author of the blogpost


import json
import socket
import requests
from block import Block

class Helper:

    # for future improvements, this proof_of_work function can also increase difficulty
    # and based on the previous hashes of the chain 
    def proof_of_work(self, last_proof):
        """
            param1 obj: self object
            param2 int: last mined block's proof-of-work

            return int: resolved new proof-of-work
        
            external api called by each server's node 
            mine method to mine a new coin with a new proof
        
        """
        if last_proof == None:
            last_proof = 1                                                      # this will result of the new proof being 9

        incrementor = last_proof + 1

        while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
            incrementor += 1
        
        return incrementor

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    class Node_helper:

        # this resolves local ip
        # public ip can be resolved by urllib request to getmyip.com or similar sites

        def _resolve_host(self):
            """
                param1 obj: self object

                return str: local(public if needed) ip of node's host

                internal api called by consensus to help remove the current host
                node in the consensus process

            
            """

            google_dns = "8.8.8.8"                                      # we will attempt to connect to google's public dns server
            google_dns_port = 80
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((google_dns, google_dns_port))
            
            ret = s.getsockname()[0]                                    # and also reading our socket info [0] is ip address
                                                                        # assuming we have internet access, and no local proxy

            s.close()

            return ret

#-------------------------------------------------------------------------------------------------------------------------------------------------

        # this can also be improved to have a security check, to ensure node integrity
        def consensus(self, peer_nodes):
            """
                param1 obj: self object
                param2 list: current peer node list
            
                return list: updated peer node's list
                
                external api called by Server._updateList
                to update this server node's peer_node list
                
                current policy: 
                    1. individually evaluate each node, and keep all the nodes we dont have
                    2. will not keep this node's host:port as one of the nodes on the network
            
            """

            add_nodes = []
            for each_server_nodes in self._find_other_nodes(peer_nodes):        # this function call returns [[S1nodes], [S2nodes], ...]

                for node in each_server_nodes:                                  # this makes sure we dont add our own ip address onto peer nodes
                    if node['host'] == self._resolve_host():
                        each_server_nodes.remove(node)

                for node in each_server_nodes:                                  # second iteration to compare
                    if not self._have_node(node, peer_nodes):
                        add_nodes.append(node)


            return self._update_nodes(peer_nodes, add_nodes)                    # remember peer_nodes is the older version to be synced

#-------------------------------------------------------------------------------------------------------------------------------------------------    
        def _find_other_nodes(self, peer):
            """
                param1 obj: self object
                param2 list: current peer_node list

                return list: list of all network's node_lists

                internal api called by consensus to return a list of 
                peer_node list
            
            
            """
            all_nodes_on_each_network = []

            for p in peer:
                response = None
                try:
                    response = requests.get('http://{}/get_nodes'.format(p))            # acquiring nodes from all other servers
                except:
                    pass

                if response is not None and response.status_code == 200:
                    all_nodes_on_each_network.append(json.loads(response.content))      # response.content is in json format, hence loading it

            return all_nodes_on_each_network



#------------------------------------------------------------------------------------------------------------------------------------------------- 
        def _have_node(self, node, my_nodes):
            """
                param1 obj: self object
                param2 dict: node dictionary that we are comparing
                param3 list: list of current peer_nodes

                return bool: whether or not current peer_nodes have the evaluated node
            
                internal api called by node consensus to check if the current peer_node list 
                contain the evaluated node
            
            """
            for n in my_nodes:
                host = node['host'] + ':' + node['port']
                if host == n:                                                           # meaning I already have this node

                    return True

            return False

#------------------------------------------------------------------------------------------------------------------------------------------------
        
        def _update_nodes(self, peer_nodes, to_be_added_nodes):
            """
                param1 obj: self object
                param2 list: current peer_nodes list
                param3 list: the list of nodes we need to add [{dict}]
            
                return list: a list of updated peer_nodes for node consensus
            
                internal api called by node consensus to return the updated peer_node list
            
            """

            for node in to_be_added_nodes:
                host = node['host'] + ':' + node['port']                                # converted back to host:port format for calling server
                peer_nodes.append(host)
            
            return peer_nodes


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    class Blockchain_helper:

        # the two methods below adds an abstraction level to the Server class, so Server does not have to deal with Block directly
        def create_gen_block(self):
            """
                param1 obj: self object

                return obj: Block class genesis block object
                
                external api called by Server.miner if needed a genesis block to kickstart the chain
            
            """
            return Block.create_genesis_block()

        def create_block(self, index, timestamp, data, prev_hash):
            """
                param1 obj: self object
                param2 int: index of the block created
                param3 str: string of the block creation time
                param4 dict: data dictionary consists of list of transactions, and proo-of-work
                param5 str: hash of the last block

                return Block class object 

                external api called by Sever.miner, for the new mined block
            
            """
            return Block(index, timestamp, data, prev_hash=prev_hash)

        # note, for future improvements, we can also add security to this function
        # by checking previous hashes of the blockchain to ensure integrity
        def consensus(self, blockchain, peernodes):
            """
                param1 obj: self object
                param2 list: list of current blockchain
                param3 list: list of current peer_nodes

                return list: updated blockchain for Server

                external api called by Server._updateList

                Current policies: 
                        1. always sync the longest chain
                        2. if same length, we sync earlier mined block's chain
            
            """
            longest_chain = blockchain
            auto_sync = False
    
            for chain in self._find_other_chains(peernodes):
                if len(longest_chain) < len(chain):                                                 # 1. take the longer chain        
                    longest_chain = chain

                elif len(longest_chain) == len(chain) and len(chain) != 0:                          # 2. autosync the earlier chain
                    auto_sync = self._compare_last(longest_chain, chain)

                    if auto_sync is True:
                        longest_chain = chain
                    else:                                                                           # meaning take our current longest chain
                        continue                                            

            # scenario when auto_sync is turned on: compared block is the same length and has an earlier mined block (last block),
            # in that case, every other node's chain when compared after, will be "auto"synced no matter what, 
            # if not this chain, or even a longer chain will need to be synced, 

            # scenario when auto_sync is turned off: when there are no same length chains with last block as a mined block, 
            # accounts for all other times if two blocks are mined/created very closely to each other, timewise. 

            return self._update_blockchain(blockchain, longest_chain, auto_update=auto_sync)
    
#-------------------------------------------------------------------------------------------------------------------------------------------------

        def _compare_last(self, current_longest_chain, chain_to_be_evaluated):
            """
                param1 obj: self object
                param2 list: current longest blockchain list from consensus 
                param3 list: same length as the longest chain, to be evaluated list

                return bool: whether or not autosync to sync the equalivated length longest chain

                internal api called by blockchain consensus to evaluate autoSync in update

                Current policies:
                        1. return false if last blocks of chains are not mined chain
                        2. return false if current_longest_chain has an earlier stamped coin
                        3. return false if current block of any chain transaction is None
                            meaning no transactions, dummy block, and we can just use our chain in that case
                        4. return true if chain_to_be_evaluated has an earlier stamped coin
            
            
            """

            # extracting data from dict
            current_chain_timestamp =  current_longest_chain[-1]["timestamp"]
            chain_to_be_evaluated_timestamp = chain_to_be_evaluated[-1]['timestamp']
            
            if current_longest_chain[-1]["data"]["transactions"] is not None:
                current_lastblock_lastTrans_from = current_longest_chain[-1]["data"]["transactions"][-1]["from"]
            else:
                return False

            if chain_to_be_evaluated[-1]["data"]["transactions"] is not None:
                evaulate_lastblock_lastTrans_from = chain_to_be_evaluated[-1]["data"]["transactions"][-1]["from"]
            else:
                return False
            
            
            # evaluation

            # if last blocks arent mined blocks
            if (current_lastblock_lastTrans_from is not "network") or (evaulate_lastblock_lastTrans_from is not "network"):
                return False

            # if the current chain timestamp is earlier than evaluated chain timestamp
            elif max(current_chain_timestamp, chain_to_be_evaluated_timestamp) is chain_to_be_evaluated_timestamp:
                return False

            # if the current chain timestamp is the later one, and we need to auto sync
            elif max(current_chain_timestamp, chain_to_be_evaluated_timestamp) is current_chain_timestamp:
                return True




#-------------------------------------------------------------------------------------------------------------------------------------------------

        def _find_other_chains(self, peer_nodes):
            """
                param1 obj: self object
                param2 list: current peer_nodes

                return list: list of blockchain lists from peers

                internal api called by blockchain consensus
            
            
            """
            chains = []
            
            for peer in peer_nodes:                                               # iterating through all peers

                response = None
                try:
                    response = requests.get('http://{}/get_blocks'.format(peer))  # retrieving blockchains from peer
                except:
                    pass

                output = "[+] Blocks from peer at {}: {}".format(peer, response.content)

                if response is not None and response.status_code == 200:

                    print output
                    chains.append(json.loads(response.content))                   # remember to load the json object to list(dict)before append
    
    
            return chains
    
#------------------------------------------------------------------------------------------------------------------------------------------------- 
        def _update_blockchain(self, blockchain, new_blockchain, auto_update=False):    
            """
                param1 obj: self object
                param2 list: current blockchain list
                param3 list: blockchain list to be updated 
                param4 bool: auto_update feature to update same length lists, default: False

                return list: updated list of blockchain
            
                internal api called by blockchain consensus
            
            """

            if len(new_blockchain) > len(blockchain) or auto_update is True:        # if the new blockchain is longer than mine
                ret = []                                                            # or if autoupdate is on, we take the new chain
                for block in new_blockchain:                                        # by converting the new chain from dict to obj

                    ret.append(Block(block['index'], block['timestamp'], block['data'], current_hash=block['hash']))

                return ret

            else:                                                                   # else, if this node's blockchain is the longest, we just ret
                return blockchain                                                       

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    class Transaction_helper:

        def consensus(self, transactions, peernodes):
            """
                param1 obj: self object
                param2 list: current list of this_node_transactions
                param3 list: current list of peer_nodes

                return list: updated list of transactions
            
                external api called by Server._updateList to update list of transactions

                current policies: 
                    1. take the longest list of transactions among peer

            """
            my_transactions = transactions                                                  # grabbing current trans list

            for peer_transactions in self._find_other_transactions(peernodes):              # iterate through each of peer's trans list
                if len(my_transactions) < len(peer_transactions):
                    my_transactions = peer_transactions                                     # if peer trans is longer than current, take peer

            return self._update_transactions(transactions, my_transactions)

#-------------------------------------------------------------------------------------------------------------------------------------------------
        
        def _find_other_transactions(self, peer_nodes):                  
            """
                param1 obj: self object
                param2 list: current list of peer_nodes

                return list: list of transaction lists among peer

                internal api called by transaction consensus 
            
            
            """
            transactions = []

            for peer in peer_nodes:
                response = None
                try:
                    response = requests.get('http://{}/get_trans'.format(peer))         # retrieving list of transactions from peer
                except:
                    pass

                if response is not None and response.status_code == 200:
                    transactions.append(json.loads(response.content))                   # all data is loaded back to dict form before returning

            return transactions

#-------------------------------------------------------------------------------------------------------------------------------------------------

        def _update_transactions(self, old_transactions, to_be_updated_transactions):
            """
                param1 obj: self object
                param2 list: list of current transactions
                param3 list: list of to be updated transactions

                return list: list of updated transactions

                internal api called by transaction consensus
            
                current policy: 
                    1. return the longest list of transaction dictionaries 
            """
            if len(to_be_updated_transactions) <= len(old_transactions):
                return old_transactions

            else:
                return to_be_updated_transactions                   # no need for conversion, because its already in the format we want for server

#-------------------------------------------------------------------------------------------------------------------------------------------------

        def ensure(self, current_transactions,  delete_list_of_trans):
            """
                param1 obj: self object
                param2 list: list of current transactions
                param3 list: list of transactions to be delete/account for

                return list: list of newly updated transactions

                external api called by Server.clear_trans_handler to ensure we account for all transcations
            
            """
            
            new_current_t = []

            for trans in current_transactions:
                if trans in delete_list_of_trans:
                    continue
                else:                                           # only append the ones that are not in the list of to be deleted transactions
                    new_current_t.append(trans)

            return new_current_t                                # returning the unaccounted transactions
            



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++










