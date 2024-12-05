import hashlib
import time
import json
from typing import List, Dict

class Block:
    def __init__(self, index: int, transactions: List[Dict], timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict] = []
        self.difficulty = 2
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

# // what is property
    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, sender: str, recipient: str, amount: float):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address: str):
        block = Block(len(self.chain), self.pending_transactions, time.time(), self.last_block.hash)
        self.proof_of_work(block)

        self.chain.append(block)
        self.pending_transactions = [
            {'sender': "Mining Reward", 'recipient': miner_address, 'amount': 1}  # Mining reward
        ]
    
    def proof_of_work(self, block: Block):
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_balance(self, address: str) -> float:
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction['sender'] == address:
                    balance -= transaction['amount']
                if transaction['recipient'] == address:
                    balance += transaction['amount']
        return balance
    
if __name__ == "__main__":
    # Create a new blockchain
    my_blockchain = Blockchain()

    # Add some transactions
    my_blockchain.add_transaction("Alice", "Bob", 50)
    my_blockchain.add_transaction("Bob", "Charlie", 300)

    # Mine the pending transactions
    my_blockchain.mine_pending_transactions("Miner1")

    # Add more transactions
    my_blockchain.add_transaction("Charlie", "David", 10)
    my_blockchain.add_transaction("David", "Eve", 100)

    # Mine again
    my_blockchain.mine_pending_transactions("Miner2")

    # Print the blockchain
    for block in my_blockchain.chain:
        print(f"Block #{block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Transactions: {block.transactions}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print("\n")

    # Check balances
    print(f"Alice's balance: {my_blockchain.get_balance('Alice')}")
    print(f"Bob's balance: {my_blockchain.get_balance('Bob')}")
    print(f"Miner1's balance: {my_blockchain.get_balance('Miner1')}")
    print(f"Miner2's balance: {my_blockchain.get_balance('Miner2')}")

    # Validate the chain
    print(f"Is blockchain valid? {my_blockchain.is_chain_valid()}")