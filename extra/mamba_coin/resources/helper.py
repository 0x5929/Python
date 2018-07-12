#!/usr/bin/python


# this file is a helper file that will be utilized in ../server.py

import json
import socket
import requests
from block import Block

class Helper:

    #NOTE: for future improvements, this proof_of_work function can also increase difficulty
    # and based on the previous hashes of the chain 
    def proof_of_work(self, last_proof):
        if last_proof == None:
            last_proof = 1                  # this will result of the new proof being 9

        incrementor = last_proof + 1

        while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
            incrementor += 1
        
        return incrementor

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    class Node_helper:

        # this resolves local ip, future improvement is to resolve public ip, if and once mamba coin is deployed
        # public ip can be resolved by urllib request to getmyip.com or similar sites

        def _resolve_host(self):

            google_dns = "8.8.8.8"                                      # we will attempt to connect to google's public dns server
            google_dns_port = 80
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((google_dns, google_dns_port))
            
            ret = s.getsockname()[0]                                    # and also reading our socket info [0] is ip address
                                                                        # assuming we have internet access, and no local proxy

            s.close()

            return ret

#-------------------------------------------------------------------------------------------------------------------------------------------------

        # sync nodes will take the most amount of nodes in network to be true
        # this can also be improved to have a security check, to ensure node integrity
        def consensus(self, peer_nodes):

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
        # called by nodes_consensus to extract peer node list from peer nodes
        def _find_other_nodes(self, peer):
            all_nodes_on_each_network = []

            for p in peer:
                response = None
                try:
                    response = requests.get('http://{}/get_nodes'.format(p))
                except:
                    pass

                if response is not None and response.status_code == 200:
                    all_nodes_on_each_network.append(json.loads(response.content))      # response.content is in json format, hence loading it

            return all_nodes_on_each_network



#------------------------------------------------------------------------------------------------------------------------------------------------- 
        def _have_node(self, node, my_nodes):
            for n in my_nodes:
                host = node['host'] + ':' + node['port']
                if host == n:                                                   # meaning I already have this node

                    return True

            return False

#------------------------------------------------------------------------------------------------------------------------------------------------
        
        # called by nodes_consensus to updated current node's back to the calling server 
        def _update_nodes(self, peer_nodes, to_be_added_nodes):

            for node in to_be_added_nodes:
                host = node['host'] + ':' + node['port']                            # converted back to host:port format for calling server
                peer_nodes.append(host)
            
            return peer_nodes


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    class Blockchain_helper:

        # note, for future improvements, we can also add security to this function
        # by checking previous hashes of the blockchain to ensure integrity
        # also we should account for two blocks mined around the same time (between first and second sync of mine api)
        # would need to honor the earliest stamped mined block's chain
        def consensus(self, blockchain, peernodes):
            longest_chain = blockchain
    
            for chain in self._find_other_chains(peernodes):
                if len(longest_chain) < len(chain):
                    longest_chain = chain

            return self._update_blockchain(blockchain, longest_chain)
    
#-------------------------------------------------------------------------------------------------------------------------------------------------
    
        # called by block_consensus to extract blockchains from peer nodes
        def _find_other_chains(self, peer_nodes):
            chains = []
            
            for peer in peer_nodes:
                reponse = None
                try:
                    response = requests.get('http://{}/get_blocks'.format(peer))
                except:
                    pass

                if response is not None and response.status_code == 200:
                    print "[+] Blocks from peer at {}: {}".format(peer, response.content)
                    chains.append(json.loads(response.content))                   # remember to load the json object to list(dict)before append
    
    
            return chains
    
#------------------------------------------------------------------------------------------------------------------------------------------------- 
        # called by block_consensus to update blockchain to calling server
        def _update_blockchain(self, blockchain, new_blockchain):                       # blockchain is mine, and in [object] format 
            if len(new_blockchain) <= len(blockchain):                                  # new_blockchain is to be updated, and from peer
                return blockchain                                                       # and is in [dict] format
            else:
                ret = []
                for block in new_blockchain:
                    # could be cleaner with the current hash, and previous hash, but all code needs to account for this
                    ret.append(Block(block['index'], block['timestamp'], block['data'], current_hash=block['hash']))
            
                return ret

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    class Transaction_helper:

        # for future improvements, we should add a checker in this function to check the vadility of all transactions, make sure 
        # no bogus transactions are present when updated
        def consensus(self, transactions, peernodes):
            my_transactions = transactions

            for peer_transactions in self._find_other_transactions(peernodes):
                if len(my_transactions) < len(peer_transactions):
                    my_transactions = peer_transactions

            return self._update_transactions(transactions, my_transactions)

#-------------------------------------------------------------------------------------------------------------------------------------------------
        
        # called by trans_consensus to extract transaction list from peer nodes
        def _find_other_transactions(self, peer_nodes):                  
            transactions = []

            for peer in peer_nodes:
                response = None
                try:
                    response = requests.get('http://{}/get_trans'.format(peer))
                except:
                    pass

                if response is not None and response.status_code == 200:
                    transactions.append(json.loads(response.content))                   # all data is loaded back to dict form before returning

            return transactions

#-------------------------------------------------------------------------------------------------------------------------------------------------

        # called by trans_consensus to update transaction list to the calling server
        def _update_transactions(self, old_transactions, to_be_updated_transactions):
            if len(to_be_updated_transactions) <= len(old_transactions):
                return old_transactions
            else:
                return to_be_updated_transactions                   # no need for conversion, because its already in the format we want for server

#-------------------------------------------------------------------------------------------------------------------------------------------------

        # called by server's /clear_trans DELETE api to ensure we don't delete unaccounted transactions
        def ensure(self, current_transactions, peernodes):

            non_synced_node_transactions = []
            unsynced_transactions = []

            # check if length is the same as other, same means we are in sync, and no problem
            for peer_transactions in self._find_other_transactions(peernodes):
                if len(current_transactions) <= len(peer_transactions):             # this means that only mining node has one more mining trans 
                    continue
                else:   # if we have more transactions than other nodes, especially mining node, meaning syncing was not successful and 
                        # probably recieved more transactions after sync and before mining node started to mine, so we need to compare the two
                        # to ensure we dont delete any new transactions after mining process is done, and these transactions will  be synced
                        # by others, so it will not be lost 
                    non_synced_node_transactions.append(peer_transactions)
                    
            longest_node_trans = None


            # making sure we ONLY compare the longest unsynced node's transaction list
            for node_trans in non_synced_node_transactions:
                try:
                    if len(node_trans) > len(non_synced_node_transactions[non_synced_node_transactions.index(node_trans) + 1]):
                        longest_node_trans = node_trans
                    else:
                        longest_node_trans = non_synced_node_transactions[non_synced_node_trans.index(node_trans) + 1]
                except IndexError:
                    pass

            if longest_node_trans is not None:
                unsynced_transactions = self._compare_trans(current_transactions, longest_node_trans)
            
            return unsynced_transactions

#-------------------------------------------------------------------------------------------------------------------------------------------------

        # called by trans_ensure to compare and extract unaccounted transactions for the calling server 
        def _compare_trans(self, my_trans, peer_trans):
            unsynced_trans = []
            for trans in my_trans:
                if trans in peer_trans:
                    continue
                else:
                    unsynced_trans.append(trans)

            return unsynced_trans

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++










