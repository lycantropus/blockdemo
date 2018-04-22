import datetime as date
import json
import random
import string
import requests
from flask import Flask
from flask import request

from block import Block
from genesis_block import create_genesis_block

node = Flask(__name__)

miner_address = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
this_node_transactions = []
blockchain = [create_genesis_block()]
peer_nodes = []
mining = True


def find_new_chains():
    other_chains = []

    for node_url in peer_nodes:
        block = requests.get(node_url + "/blocks").content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains


def consensus():
    other_chains = find_new_chains()
    longest_chain = blockchain

    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    blockchain = longest_chain


@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_txion = request.get_json()
        this_node_transactions.append(new_txion)
        return "TRANSACTION SUBMITTED"


def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 6 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor


@node.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']
    proof = proof_of_work(last_proof)
    this_node_transactions.append(
        {"from": "network", "to": miner_address, "amount": 1}
    )

    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_node_transactions)
    }

    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    this_node_transactions[:] = []

    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )

    blockchain.append(mined_block)

    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": last_block_hash
    }) + "\n"


@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = blockchain

    blocklist = ""

    for i in range(len(chain_to_send)):
        block = chain_to_send[i]
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        assembled_block = json.dumps({
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
        }) + "\n"

        if blocklist == "":
            blocklist = assembled_block
        else:
            blocklist += assembled_block

    return blocklist

node.run(host='0.0.0.0')
