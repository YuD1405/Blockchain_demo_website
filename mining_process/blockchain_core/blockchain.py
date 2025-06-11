import hashlib
import json
import time
from blockchain_core.transaction import MerkleTree, Transaction

class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=None):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.nonce = 0
        self.merkle_root = MerkleTree(transactions).get_root()
        
    def compute_hash(self):
        # Chuyển đổi các thông tin của block thành dạng hex
        # index: chuyển thành hex, bỏ đi "0x"
        index_hex = hex(self.index)[2:]
        
        # previous_hash: giả sử đã ở dạng hex
        previous_hash_hex = self.previous_hash
        
        # timestamp: chuyển thành số nguyên (nếu cần) rồi thành hex
        timestamp_hex = hex(int(self.timestamp))[2:]
        
        # nonce: chuyển thành hex
        nonce_hex = hex(self.nonce)[2:]
        
        # merkle_root: đã ở dạng hex
        merkle_root_hex = self.merkle_root

        # Gộp tất cả các chuỗi hex lại thành một chuỗi lớn
        combined = index_hex + previous_hash_hex + nonce_hex + merkle_root_hex # + timestamp_hex: không cần time để thực hành, thực tế thì cần

        # Hash lần thứ nhất: chuyển chuỗi thành bytes rồi hash bằng SHA-256
        hash1 = hashlib.sha256(combined.encode()).hexdigest()
        
        # Hash lần thứ hai: hash lại kết quả của hash1
        hash2 = hashlib.sha256(hash1.encode()).hexdigest()
        return hash2
    
    def print_block(self):
        print(f"Block Index: {self.index}")
        print(f"Previous Hash: {self.previous_hash}")
        print(f"Merkle Root: {self.merkle_root}")
        print(f"Nonce: {self.nonce}")
        print(f"Hash: {self.compute_hash()}")
        print("\n--- Transactions ---")
        for tx in self.transactions:
            tx.print_transaction()
            print("-" * 30)
        
class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = difficulty
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, [], "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def add_block(self, block):
        if block.previous_hash != self.chain[-1].compute_hash():
            return False
        self.chain.append(block)
        return True
    
    def print_blockchain(self):
        print("\n========== Blockchain ==========")
        for block in self.chain:
            block.print_block()
            print("-------------------------------------------------")