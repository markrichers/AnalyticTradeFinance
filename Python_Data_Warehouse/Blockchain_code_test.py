import unittest
import time
from Blockchain_code import Block, Blockchain

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()

    def test_genesis_block(self):
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)
        self.assertEqual(self.blockchain.chain[0].previous_hash, "0")

    def test_add_transaction(self):
        self.blockchain.add_transaction("Alice", "Bob", 50)
        self.assertEqual(len(self.blockchain.pending_transactions), 1)
        self.assertEqual(self.blockchain.pending_transactions[0]['sender'], "Alice")
        self.assertEqual(self.blockchain.pending_transactions[0]['recipient'], "Bob")
        self.assertEqual(self.blockchain.pending_transactions[0]['amount'], 50)

    def test_mine_pending_transactions(self):
        self.blockchain.add_transaction("Alice", "Bob", 50)
        self.blockchain.mine_pending_transactions("Miner1")
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(len(self.blockchain.pending_transactions), 1)  # Mining reward
        self.assertEqual(len(self.blockchain.pending_transactions), 1)  # Mining reward
        self.assertEqual(self.blockchain.pending_transactions[0]['recipient'], "Miner1")

    # def test_blockchain_validity(self):
    #     self.blockchain.add_transaction("Alice", "Bob", 50)
    #     self.blockchain.mine_pending_transactions("Miner1")
    #     self.assertTrue(self.blockchain.is_chain_valid())

    #     # Tamper with a block
    #     self.blockchain.chain[1].transactions[0]['amount'] = 100
    #     self.assertFalse(self.blockchain.is_chain_valid())


    def test_get_balance(self):
        self.blockchain.add_transaction("Alice", "Bob", 50)
        self.blockchain.mine_pending_transactions("Miner1")
        self.blockchain.add_transaction("Bob", "Charlie", 30)
        self.blockchain.mine_pending_transactions("Miner2")

        self.assertEqual(self.blockchain.get_balance("Alice"), -50)
        self.assertEqual(self.blockchain.get_balance("Bob"), 20)
        self.assertEqual(self.blockchain.get_balance("Charlie"), 30)
        self.assertEqual(self.blockchain.get_balance("Miner1"), 1)
        self.assertEqual(self.blockchain.get_balance("Miner2"), 1)

    def test_proof_of_work(self):
        block = Block(1, [{"sender": "Alice", "recipient": "Bob", "amount": 50}], time.time(), "previous_hash")
        self.blockchain.proof_of_work(block)
        self.assertTrue(block.hash.startswith('0' * self.blockchain.difficulty))

if __name__ == '__main__':
    unittest.main()