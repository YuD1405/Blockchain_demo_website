from flask import Flask, render_template, request, jsonify
from blockchain_core.blockchain import Blockchain, Block
from blockchain_core.transaction import Transaction
from blockchain_core.PoW import mine_block

app = Flask(__name__)

# Khởi tạo blockchain
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('mining.html', blockchain=blockchain.chain)

@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    transactions = [
        {'sender': tx.sender, 'recipient': tx.recipient, 'amount': tx.amount}
        for tx in blockchain.pending_transactions
    ]
    return jsonify({'transactions': transactions})

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    sender = data.get('sender')
    recipient = data.get('recipient')
    amount = data.get('amount')

    if not sender or not recipient or amount is None:
        return jsonify({'error': 'Thiếu thông tin giao dịch'}), 400

    new_transaction = Transaction(sender, recipient, amount)
    blockchain.pending_transactions.append(new_transaction)
    return jsonify({'message': 'Giao dịch được thêm thành công'})

@app.route('/mine', methods=['POST'])
def mine():
    if not blockchain.pending_transactions:
        return jsonify({'error': 'Không có giao dịch để mine'}), 400

    new_block = mine_block(blockchain.chain[-1], blockchain.pending_transactions)
    blockchain.add_block(new_block)
    
    blockchain.pending_transactions = []
    return jsonify({'message': 'Block mới đã được mine', 'block_index': new_block.index})

@app.route('/latest_block', methods=['GET'])
def latest_block():
    latest = blockchain.chain[-1]
    return jsonify({
        'index': latest.index,
        'nonce': latest.nonce,
        'previous_hash': latest.previous_hash,
        'merkle_root': latest.merkle_root,
        'hash': latest.compute_hash(),
        'difficulty': blockchain.difficulty
    })
    
if __name__ == '__main__':
    app.run(debug=True)
