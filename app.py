from flask import Flask
from flask import request
from flask import jsonify
import sqlite3

app = Flask(__name__)
transactions = []

@app.route("/")
def hello():
    print("Home route was hit")
    return "Personal Finance API is running"

# User input of transactions. POST function.
@app.route('/transactions', methods=['POST'])
def userInput():
    # Get JSON
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Data field empty"}), 400
    con = get_db_connection()
    cursor = con.cursor()
    # Parsing data values. Extract.
    amount = data.get("amount")
    category = data.get("category")
    transaction_type = data.get("transactionType")
    # Validate
    if amount is None or category is None or transaction_type is None:
        return jsonify({"error": "Missing required fields"}), 400
    # Transaction dictionary initialized.
    # transaction = {
    #   "id": len(transactions) + 1,
    #   "amount": amount,
    #    "category": category,
    #    "transactionType": transaction_type
    #}
    # transactions.append(transaction)
    cursor.execute("""INSERT INTO transactions(amount, category, transactionType) VALUES (?,?,?)""", (amount, category, transaction_type))
    con.commit()
    con.close()
    # Debug print for successful insertion.
    # print("Successfully Inserted")
    # print(amount, category, transaction_type)
    return jsonify({"message": "Transaction added successfully"}), 201

# User output of GET request for transactions.
@app.route('/transactions', methods=['GET'])
def outputTransactions():
    con = get_db_connection()
    # Retrieve data from table and store it in list.
    transaction = {}
    data = con.execute('SELECT * FROM transactions')
    # fetch rows.
    rows = data.fetchall()
    # make empty result list.
    result = []
    # for each row.
    for row in rows:
        # make transaction dictionary from row values.
        transaction = {
            "id": row[0],
            "amount": row[1],
            "category": row[2],
            "transactionType": row[3]
        }
        result.append(transaction)
    return jsonify(result)
    con.close()
    return jsonify({"message": "Displayed all transactions."})

# User GET request for transaction by Id.
@app.route('/transactions/<int:id>', methods=['GET'])
def outputTransactionsByID(id):
    con = get_db_connection()
    data = con.execute(
        'SELECT id, amount, category, transactionType FROM transactions WHERE id = ?',
        (id,)
    )
    result = data.fetchone()
    
    if result is None:
        con.close()
        return jsonify({"message": "Id not found."}), 404
    
    transaction = {
        "id": result[0],
        "amount": result[1],
        "category": result[2],
        "transactionType": result[3]
    }
    
    con.close()
    return jsonify(transaction)

# User DELETE request for deleting transactions.
@app.route('/transactions/<int:id>', methods=['DELETE'])
def delTransactionsByID(id):
    con = get_db_connection()
    data = con.execute(
        'SELECT id, amount, category, transactionType FROM transactions WHERE id = ?',
        (id,)
    )
    result = data.fetchone()
    if result is None:
        con.close()
        return jsonify({"message": "Id not found."}), 404
    # Delete row.
    con.execute(
        'DELETE FROM transactions WHERE id = ?',
        (id,)
    )
    con.commit()
    con.close()    
    return jsonify({"message": "Transaction deleted successfully."}), 200

@app.route('/transactions/<int:id>', methods=['PUT'])
def changeTransactionInfoById(id):
    # Check if row exists.
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Missing required data field."}), 400
    # Parse new data.
    amount = data.get("amount")
    category = data.get("category")
    transaction_type = data.get("transactionType")
    # Check if any data is missing.
    if amount is None or category is None or transaction_type is None:
        return jsonify({"error": "Missing data field."}), 400
    
    con = get_db_connection()
    # Check if row exists.
    check = con.execute(
        'SELECT id, amount, category, transactionType FROM transactions WHERE id = ?',
        (id,)
    )
    # Get row.
    result = check.fetchone()
    # Check if row is empty.
    if result is None:
        con.close()
        return jsonify({"error": "Could not update."}), 404
    # Update row.
    con.execute(
        'UPDATE transactions SET amount = ?, category = ?, transactionType = ? WHERE id = ?',
        (amount, category, transaction_type, id)
    )
    con.commit()
    con.close()
    
    return jsonify({"message": "Transaction updated successfully."}), 200

# Database connection function.
def get_db_connection():
   con = sqlite3.connect("finance.db")
   con.row_factory = sqlite3.Row
   return con

# Setup for Database Structure. Create table for transactions if one does not already exist.
def init_db():
    con = sqlite3.connect("finance.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY, amount REAL, category TEXT, transactionType TEXT)")
    con.commit()
    con.close()


if __name__ == "__main__":
    init_db()
    app.run(debug=False, use_reloader=False)