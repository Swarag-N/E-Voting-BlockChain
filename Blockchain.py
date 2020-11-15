from urllib.parse import urlparse
import json
from time import time
import requests
import hashlib
from uuid import uuid4
from datetime import datetime



class Blockchain(object):
    # This method acts as a contrcutor for the blockchain
    #  Data Structure of the Block is at  New Block Definition
    def __init__(self):
        # To have the number of votes have been cast
        self.current_transactions = []
        # chain indicates all the blocks in current leading chain in the code 
        self.chain = []
        # All the nodes which participate in consesus are stored
        self.nodes = set()
        # New Block to be added to the Chain
        self.new_block(previous_hash=1, proof=100)

    # Proof of validation occurs on every block to cross check on reolving nodes
    @staticmethod
    def valid_proof(last_proof, proof):
        # We take a proofs of last blocks and hash them using sh256 lib
        guess = f'{last_proof}{proof}'.encode()
        # After encoding the value we convert that into hexdigest form. 
        guess_hash = hashlib.sha256(guess).hexdigest()
        # we use ending zero as a topic o f validation wif wqanterd to increathe security or protection of the 
        # block chain we can add more zeros according to that
        return guess_hash[:2] == "00"

    # Hashing is the core concept of the blockchain, every block and 
    # every instace of block chain happens on the conncept of the blockchain 
    @staticmethod
    def hash(block):
        # Bloks in the Blockhain happen to be tored in JSON or python libraries which are not 
        # feasible to be hashed with the space caharcters so we encode those python dictonaries or JSON objects 
        # into a string and hash. (Using sha256)
        stringfied_block = json.dumps(block, sort_keys=True).encode()
        # Returning the hashed value
        return hashlib.sha256(stringfied_block).hexdigest()

    # It is a best practise to most used ptoperties of an Object as properties
    # As they amke understanding code much easier and reading to
    @property
    def rear_block(self):
        # Last block of the chain will have an index of -1 in an array
        return self.chain[-1]

    # Node registration is place where core concept of Consenus happens,
    def node_registration(self, address):
        # Row url cannot be used directky for prossing the routes, so we do 
        # url cheking, ike we verify the input to a url string
        url_parsed = urlparse(address)
        # the parsed url , if it is genuine id, we will append that node
        # url to the our block chain and on further verficatiins we use that
        # to resolve nodes
        self.nodes.add(url_parsed.netloc)

    # Resolve conflicts is used it for verification purposes 
    def resolve_conflicts(self):
        #   we take the values which are already kept in the run time of the server
        neighbour_servers = self.nodes
        #then start a new temporary chain to verify whether the nodes there on the 
        # server and chain coming from other nodes match 
        temp_new_chain = None
        # length of the current chain plays a major role in the verification
        length_current_chain = len(self.chain)

        # Each node from neighbouring servers are collected and used
        for node in neighbour_servers:
            # Request is sent to all the neighbouring nodes for the change in the chain
            response = requests.get(f'http://{node}/chain')

            # Depending upon the status code of the response the further of application is done
            if response.status_code == 200:
                # Data like chain chain length last block which are in the current response details are used for verification process
                chain_length = response.json()['length']
                chain = response.json()['chain']
                #  initial cases changes determines the major priority are from the chain length 
                # that is if chain length 
                # less than the curent length of the challenge is present in the power change 
                # is to be replaced by the small to longest chain
                if chain_length > length_current_chain and self.validate_chain(chain):
                    length_current_chain = chain_length
                    temp_new_chain = chain
        if temp_new_chain:
            self.chain = temp_new_chain
            return True

        return False

    #  This below funtion is invoked when creating a new block
    def new_block(self, proof, previous_hash=None):
        # Data structure of the block can be seen below
        block = {
            'index': len(self.chain) + 1, #Index is stored in Block
            'timestamp': time(), #Timestamp is in UNIX
            'transactions': self.current_transactions, #Transactions here mean the voting data (data structure at new transaction)
            'proof': proof, #Proof the the block is used at the tie of mining
            'previous_hash': previous_hash or self.hash(self.chain[-1]), #THis the hash of preivous blocks
        }

        # Since we are initaing the block, all the current transaction s are therefore flused
        self.current_transactions = []
        # Old block is that is the newly forged block is added to chain
        self.chain.append(block)
        # New block is again set to veriyf the timesatmps and  other stuff
        return block

    # A new transaction is added  to the current trancations of the chain which are not added to the chain until mined into a block
    def new_transaction(self, Party_A, Party_B, Votes):
        # New transcations takes 3 prameters such as PartyA , PartyB which are the party codes of the Leading and Runnerup 
        # Contestants  and the last parameter is the the Votes which is the dufference of votes by which the leading Contestant gas won the
        # election in the mandal Election 
        self.current_transactions.append({
            'Party_A': Party_A, #Leading Contestants PARTY_ID or Contestant ID
            'Party_B': Party_B, # Runner Up Contestants PARTY_ID or Contestant ID
            'Votes': Votes,#The count of the number of votes, the Leading Contestant from the Runner Up Position
        })
        # Modifiyng the deatils in the Rear Block of the chain
        return self.rear_block['index'] + 1

    # Proof of Work is the heart and soul of blockchain concept,
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        print(proof)
        return proof

    # Chain Validation, is very important concept of validation. 
    # When randomm requests to server mare made to server with rubbish dayta, all the legal and genuine data will be replaced
    # to counter this we verify every block of the blockchain before making changes 
    def validate_chain(self, chain):
        # Rear block is the main block to be verifried before doing any other operations
        rear_block = chain[0]
        live_index = 1

        while live_index < len(chain):
            block = chain[live_index]
            print(f'{rear_block}')
            print(f'{block}')
            print("\n-----------\n")
            if block['previous_hash'] != self.hash(rear_block):
                return False
            if not self.valid_proof(rear_block['proof'], block['proof']):
                return False

            rear_block = block
            live_index += 1

        return True
