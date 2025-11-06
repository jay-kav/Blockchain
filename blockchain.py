import hashlib
import json
from time import time

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