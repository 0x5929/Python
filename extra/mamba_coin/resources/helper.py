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

        # the two methods below adds an abstraction level to the Server class, so Server does not have to deal with Block
        def create_gen_block(self):
            """
                called by Server.miner if needed a genesis block to kickstart the chain
            
            """
            return Block.create_genesis_block()

        def create_block(self, index, timestamp, data, prev_hash):
            """
                called by Sever.miner, for the new mined block
            
            """
            return Block(index, timestamp, data, prev_hash=prev_hash)

        # note, for future improvements, we can also add security to this function
        # by checking previous hashes of the blockchain to ensure integrity
        # also we should account for two blocks mined around the same time (between first and second sync of mine api)
        # would need to honor the earliest stamped mined block's chain
        def consensus(self, blockchain, peernodes):
            """
                Current policies: 
                        1. always sync the longest chain
                        2. if same length, we sync earlier mined block's chain
                        3. if same length, and last blocks arent mined block, 
                            we pass
            
            """
            longest_chain = blockchain
            auto_sync = False
    
            for chain in self._find_other_chains(peernodes):
                if len(longest_chain) < len(chain):
                    longest_chain = chain

                # could be most of the case, but could be rare when two coins are mined closely
                elif len(longest_chain) == len(chain) and len(chain) != 0:
                    auto_sync = self._compare_last(longest_chain, chain)

                    if auto_sync is True:
                        longest_chain = chain
                    else:                           # meaning we still take our current longest chain
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
                Current policies:
                        1. return false if last blocks of chains are not mined chain
                        2. return false if current_longest_chain has an earlier stamped coin
                        3. return false if current block of any chain transaction is None
                            meaning no transactions, dummy block, and we can just use our chain in that case
                        4. return true if chain_to_be_evaluated has an earlier stamped coin
            
            
            """
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
            

            if (current_lastblock_lastTrans_from is not "network") or (evaulate_lastblock_lastTrans_from is not "network"):
                return False
            # note taking the max of two timestamps will return the later stamped one
            elif max(current_chain_timestamp, chain_to_be_evaluated_timestamp) is chain_to_be_evaluated_timestamp:
                return False
            # below condition means the current chain timestamp is the later one, and we need to auto sync
            # the chain that is being evaluated 
            elif max(current_chain_timestamp, chain_to_be_evaluated_timestamp) is current_chain_timestamp:
                return True




#-------------------------------------------------------------------------------------------------------------------------------------------------

        # called by block_consensus to extract blockchains from peer nodes
        def _find_other_chains(self, peer_nodes):
            chains = []
            
            for peer in peer_nodes:
                response = None
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
        def _update_blockchain(self, blockchain, new_blockchain, auto_update=False):    

            if len(new_blockchain) > len(blockchain) or auto_update is True:        # if the new blockchain is longer than mine
                ret = []                                                            # or if autoupdate is on, we take the new chain
                for block in new_blockchain:                                        # by converting the new chain from dict to obj

                    ret.append(Block(block['index'], block['timestamp'], block['data'], current_hash=block['hash']))

                return ret

            else:                                                                   # else, if this node's blockchain is the longest, we just ret
                return blockchain                                                       

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
        # simplified from original design 
        def ensure(self, current_transactions,  delete_list_of_trans):
            
            new_current_t = []

            for trans in current_transactions:
                if trans in delete_list_of_trans:
                    continue
                else:                                           # only append the ones that are not in the list of to be deleted transactions
                    new_current_t.append(trans)

            return new_current_t                                # returning the unaccounted transactions
            



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++










