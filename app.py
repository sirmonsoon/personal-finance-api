from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)
transactions = []

@app.route("/")
def hello():
    print("Home route was hit")
    return "Personal Finance API is running"

# User input of transactions.
@app.route('/transactions', methods=['POST'])
def userInput():
    # Get JSON
    data = request.get_json()
    # Parsing data values. Extract.
    amount = data.get("amount")
    category = data.get("category")
    transaction_type = data.get("transactionType")
    # Validate
    if amount is None or category is None or transaction_type is None:
        return "Error"
    # Transaction dictionary initialized.
    transaction = {
        "id": len(transactions) + 1,
        "amount": amount,
        "category": category,
        "transactionType": transaction_type
    }
    transactions.append(transaction)
    print(amount, category, transaction_type)
    return transaction

# User output of GET request for transactions.
@app.route('/transactions', methods=['GET'])
def outputTransactions():
    return jsonify(transactions)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)