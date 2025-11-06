import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

        def new_block(self):
            """Create a new Block in the Blockchain"""

            block = {
                'index': len(self.chain) + 1,
                'timestamp': time(),
                'transactions': self.current_transactions,
                'proof': proof,
                'previous_hash': previous_hash or self.hash(self.chain[-1]),
            }

            # Reset the current list of transactions
            self.current_transactions = []
            self.chain.append(block)
            return block

        def new_transcation(self):
            pass

        #static used to indicate that this method does not depend on the instance and is just a utility function living inside the class
        @staticmethod
        def hash(block):
            """Creates a SHA-256 hash of a Block"""
            # Make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
            block_string = json.dumps(block, sort_keys=True).encode()
            return hashlib.sha256(block_string).hexdigest()
        


        def new_transaction(self, sender, recipient, amount):
            """
             `Creates a new transaction to go into the next mined Block`
             :param sender: <str> Address of the Sender
             :param recipient: <str> Address of the Recipient
             :param amount: <int> Amount
             :return: <int> The index of the Block that will hold this transaction
             """

            self.current_transactions.append({
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            })
    
            return self.last_block['index'] + 1

        # Used to make a method act like an attribute provoding a getter method
        @property
        def last_block(self):
            """Returns the last Block in the chain"""
            return self.chain[-1]
        
        def proof_of_work(self, last_proof):
            """
            Simple Proof of Work Algorithm:
             - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
             - p is the previous proof, and p' is the new proof
            :param last_proof: <int>
            :return: <int>
            """

            proof = 0
            while self.valid_proof(last_proof, proof) is False:
                proof += 1

            return proof
        
        def valid_proof(self, last_proof, proof):
            """ Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?"""

            guess = f'{last_proof}{proof}'.encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            return guess_hash[:4] == "0000"
        
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Reward for finding the proof
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return json.dumps(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return json.dumps(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return json.dumps(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)