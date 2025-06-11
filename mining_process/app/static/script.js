function fetchTransactions() {
    fetch('/get_transactions')
        .then(response => response.json())
        .then(data => {
            const transactionList = document.getElementById("transactionList");
            transactionList.innerHTML = "";
            data.transactions.forEach(tx => {
                let li = document.createElement("li");
                li.classList.add("list-group-item");
                li.textContent = `${tx.sender} ➝ ${tx.recipient}: ${tx.amount}`;
                transactionList.appendChild(li);
            });
        });
}
document.getElementById("transactionForm").addEventListener("submit", function(event) {
    event.preventDefault();
    let sender = document.getElementById("sender").value;
    let recipient = document.getElementById("recipient").value;
    let amount = document.getElementById("amount").value;

    fetch('/add_transaction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sender, recipient, amount })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
        fetchTransactions();
    });
});

function fetchLatestBlock() {
    fetch('/latest_block')  
        .then(response => response.json())
        .then(data => {
            document.getElementById("index").value = data.index;
            document.getElementById("nonce").value = data.nonce;
            document.getElementById("prev-hash").value = data.previous_hash;
            document.getElementById("Merkle").value = data.merkle_root;
            document.getElementById("hash").value = data.hash;
            document.getElementById("difficulty").value = data.difficulty;
        });
}

document.getElementById("mineButton").addEventListener("click", function() {
    fetch('/mine', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchLatestBlock();
        location.reload();
    });
});

fetchTransactions();