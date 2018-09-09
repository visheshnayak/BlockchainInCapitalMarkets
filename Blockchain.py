import hashlib
from time import time
from urllib.parse import urlparse
from uuid import uuid4

#
#	Defines the blockchain class to be used to create the Blockchain
#	that will hold the contents of all market transactions
#
class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # Create the genesis block
        self.new_block(previous_hash='1')

	#
	#	Appends a new transaction to the collection of the current_transactions with the params
	#		buyer: holds the buyerid
	#		seller: holds the sellerid
	#		quantity: holds the number of stocks
	#		price: total price of the transactions
	#
    def new_transaction(self, buyer, seller, quantity, price) :
        self.current_transactions.append({
            'buyer': buyer,
            'seller': seller,
            'quantity': quantity,
			'price': price
        })

        return self.last_block['index'] + 1

	#
	#	creates a new block holding the following transactions
	#		index: all the indexes
	#		timestammp: the time of creation
	#		transaction: the transaction
	#		previous_hash: name itself
	#
    def new_block(self, previous_hash):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transaction': self.current_transactions,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        #
        # Creates a SHA-256 hash of a Block
        # :param block: Block
        #

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
