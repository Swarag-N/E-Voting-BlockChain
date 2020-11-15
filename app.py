#getting packages
import requests
from uuid import uuid4
from flask import Flask, jsonify, request
from datetime import datetime
#ngrok for running for server
from flask_ngrok import run_with_ngrok
from time import time
#importing blockcahin as basic implimentation
from Blockchain import Blockchain
from urllib.parse import urlparse

#naming the app system as voting
voting = Flask(_name_)

identifier_node = str(uuid4()).replace('-', '')
blockchain = Blockchain()
##run_with_ngrok(voting)

# intial root route 
@voting.route('/')
def index_route():
    return 'Blockchain Crypto'

# node to resolve the changes done in the transactions of all servers
@voting.route('/nodes/resolve', methods=['GET'])
# loading the consensus algo
def consensus():
#defining the chaned Block
    changed = blockchain.resolve_conflicts()
#respective responses of the changes nodes
    if changed:
        response = {
            'message': 'Our chain was changed',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authentic',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

#route for to allow the changed route mining them

@voting.route('/mine', methods=['GET'])
def mining_block():
    final_block = blockchain.rear_block
    last_proof = final_block['proof']

    proof = blockchain.proof_of_work(last_proof)
#checking the proof of work
    block = blockchain.new_block(proof)
    print(proof * last_proof)
#implemented to see the found blocks
    response = {
        'message': "Changed a NEW Block",
#display responces
        'index': block['index'],
        'transactions': block['transactions'],
#doing the consensus algo with overall the chain
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'done_at': datetime.fromtimestamp(block["timestamp"]),
    }
    return jsonify(response), 200

#route for new transaction in the sense the adding of new party  in voting system


@voting.route('/transactions/new', methods=['POST'])
def add_transaction():
#storing the transaction
    values = request.get_json()
#adding parties
    required = ['Party_A', 'Party_B', 'Votes']

    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(
        values['Party_A'], values['Party_B'], values['Votes'])

    response = {'message': f'Transaction is  appended to Block {index}'}
    return jsonify(response), 201

# node to register the all the servers
@voting.route('/nodes/register', methods=['POST'])
def recored_register_nodes():
    value_data = request.get_json()
#recoding the registered nodes
    nodes = value_data.get('nodes')
    if nodes is None:
        return "Error:incorrect! give a correct array of nodes", 400

    for node in nodes:
        blockchain.node_registration(node)

    response = {
        'message': 'Registedred a New',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

#route to see the final chain

@voting.route('/chain', methods=['GET'])

def retrive_whole_chain():
    response = {
        'full_chain': blockchain.chain,
        'whole_length': len(blockchain.chain),
    }
    return jsonify(response), 200


if _name_ == '_main_':
    voting.run(host='0.0.0.0')



















import requests
from flask import Flask, jsonify, request
from urllib.parse import urlparse
from uuid import uuid4
from time import time
from datetime import datetime
from flask_ngrok import run_with_ngrok
from Blockchain import Blockchain


voting = Flask(__name__)


node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()


@voting.route('/')
def index_route():
    return 'Blockchain Crypto'


@voting.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


@voting.route('/mine', methods=['GET'])
def block_mining():
    last_block = blockchain.rear_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    block = blockchain.new_block(proof)
    print(proof * last_proof)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'done_at': datetime.fromtimestamp(block["timestamp"]),
    }
    return jsonify(response), 200


@voting.route('/transactions/new', methods=['POST'])
def add_transaction():
    values = request.get_json()
    required = ['Party_A', 'Party_B', 'Votes']

    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(
        values['Party_A'], values['Party_B'], values['Votes'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@voting.route('/nodes/register', methods=['POST'])
def recored_register_nodes():
    value_data = request.get_json()

    nodes = value_data.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.node_registration(node)

    response = {
        'message': 'New has been Registered',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@voting.route('/chain', methods=['GET'])
def get_full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


if __name__ == '__main__':
    voting.run(host='0.0.0.0')


