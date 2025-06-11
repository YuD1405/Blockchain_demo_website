from blockchain_core.blockchain import Block
import blockchain_core.config as config

def mine_block(previous_block, transactions):
    index = previous_block.index + 1
    new_block = Block(index, transactions, previous_block.compute_hash())
    
    while not new_block.compute_hash().startswith('0' * config.DIFFICULTY):
        new_block.nonce += 1
    
    return new_block
