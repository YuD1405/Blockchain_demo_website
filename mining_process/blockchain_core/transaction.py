import hashlib

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def compute_hash(self):
        return hashlib.sha256(f"{self.sender}{self.recipient}{self.amount}".encode()).hexdigest()
    
    def print_transaction(self):
        print(f"Sender: {self.sender}\nRender: {self.recipient}\nAmount: {self.amount}")

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = [tx.compute_hash() for tx in transactions]

    def get_root(self):
        if not self.transactions:
            return ''

        # Tính hash của từng giao dịch
        tx_hashes = self.transactions
        
        # Xây dựng cây Merkle
        while len(tx_hashes) > 1:
            # Nếu số lượng hash lẻ, nhân đôi hash cuối cùng
            if len(tx_hashes) % 2 != 0:
                tx_hashes.append(tx_hashes[-1])
            
            new_level = []
            # Ghép đôi và tính hash cho mỗi cặp
            for i in range(0, len(tx_hashes), 2):
                combined = tx_hashes[i] + tx_hashes[i+1]
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_level.append(new_hash)
            tx_hashes = new_level
        
        return tx_hashes[0]