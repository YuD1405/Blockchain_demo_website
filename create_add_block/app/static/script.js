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

document.getElementById("mineButton").addEventListener("click", function() {
    fetch('/mine', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
        fetchTransactions();
    });
});
fetchTransactions();