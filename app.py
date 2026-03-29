from flask import Flask
from flask import request
from flask import jsonify
import sqlite3

app = Flask(__name__)
transactions = []

@app.route("/")
def welcome():
    print("Welcome.")
    return "Personal Finance API is running"

# User input of transactions. POST function.
@app.route('/transactions', methods=['POST'])
def userInput():
    # Get JSON request and store in a variable.
    data = request.get_json()
    # Data validation.
    if data is None:
        return jsonify({"error": "Data field empty"}), 400
    con = get_db_connection()
    cursor = con.cursor()
    # Parsing data values. Extract and store in separate variables.
    amount = data.get("amount")
    category = data.get("category")
    transaction_type = data.get("transactionType")
    # Validate if any fields entered are empty.
    if amount is None or category is None or transaction_type is None:
        return jsonify({"error": "Missing required fields"}), 400
    # Old method.
    # Transaction dictionary initialized.
    # transaction = {
    #   "id": len(transactions) + 1,
    #   "amount": amount,
    #    "category": category,
    #    "transactionType": transaction_type
    #}
    # transactions.append(transaction)
    # Enter data into the table.
    cursor.execute("""INSERT INTO transactions(amount, category, transactionType) VALUES (?,?,?)""", (amount, category, transaction_type))
    con.commit()
    con.close()
    # Debug print for successful insertion.
    # print("Successfully Inserted")
    # print(amount, category, transaction_type)
    return jsonify({"message": "Transaction added successfully"}), 201

# Get function to return stored transactions.
@app.route('/transactions', methods=['GET'])
def outputTransactions():
    # connect to database.
    con = get_db_connection()
    # Retrieve data from table and store it in list.
    transaction = {}
    # Get all transactions from table and store in a varible.
    data = con.execute('SELECT * FROM transactions')
    # fetch all rows.
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
        # Add dictionary objects to the result list.
        result.append(transaction)
    return jsonify(result)
    con.close()
    # Return for testing.
    # return jsonify({"message": "Displayed all transactions."})

# Function to search transactions in the database by Id.
@app.route('/transactions/<int:id>', methods=['GET'])
def outputTransactionsByID(id):
    con = get_db_connection()
    # Check if row corresponding to the Id exists in the table.
    data = con.execute(
        'SELECT id, amount, category, transactionType FROM transactions WHERE id = ?',
        (id,)
    )
    # Get row from table and store in a variable.
    result = data.fetchone()
    
    # Validation check for row.
    if result is None:
        con.close()
        return jsonify({"message": "Id not found."}), 404
    
    # Put data from row in a transaction dictionary.
    transaction = {
        "id": result[0],
        "amount": result[1],
        "category": result[2],
        "transactionType": result[3]
    }
    
    con.close()
    return jsonify(transaction)

# Function to delete transactions by Id.
@app.route('/transactions/<int:id>', methods=['DELETE'])
def delTransactionsByID(id):
    con = get_db_connection()
    # Search database by Id and return row.
    data = con.execute(
        'SELECT id, amount, category, transactionType FROM transactions WHERE id = ?',
        (id,)
    )
    # Store data from row in a variable.
    result = data.fetchone()
    # If row data is empty, send error message.
    if result is None:
        con.close()
        return jsonify({"message": "Id not found."}), 404
    # Delete row after validation.
    con.execute(
        'DELETE FROM transactions WHERE id = ?',
        (id,)
    )
    con.commit()
    con.close()    
    return jsonify({"message": "Transaction deleted successfully."}), 200

# Function to edit transaction details after searching through database using Id parameter.
@app.route('/transactions/<int:id>', methods=['PUT'])
def changeTransactionInfoById(id):
    # Check if data entered is valid.
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Missing required data field."}), 400
    # Store new data from user in their own separate variables.
    amount = data.get("amount")
    category = data.get("category")
    transaction_type = data.get("transactionType")
    # Data validation before editing the database.
    if amount is None or category is None or transaction_type is None:
        return jsonify({"error": "Missing data field."}), 400
    
    con = get_db_connection()
    # Check if row exists in database and store the returned cursor object in a variable.
    check = con.execute(
        'SELECT id, amount, category, transactionType FROM transactions WHERE id = ?',
        (id,)
    )
    # Get data from the cursor object obtained above and store in a variable.
    # fetchone() returns a single row (tuple) OR None if no result.
    result = check.fetchone()
    # Check if row is empty. Data validation.
    if result is None:
        con.close()
        return jsonify({"error": "Could not update."}), 404
    # Update database with new values from the stored variables using a returned cursor object.
    con.execute(
        'UPDATE transactions SET amount = ?, category = ?, transactionType = ? WHERE id = ?',
        (amount, category, transaction_type, id)
    )
    con.commit()
    con.close()
    
    return jsonify({"message": "Transaction updated successfully."}), 200

# Function to return a summary of transaction categories and their sum.
@app.route('/summary', methods=['GET'])
def getSummary():
    con = get_db_connection()
    
    # Group rows by category and store the cursor object in a variable.
    # The query also sums up the "amount" section from each corresponding "category" column.
    # data is a pointer to the result set produced by the SQL query.
    data = con.execute(
        'SELECT category, SUM(amount) AS total FROM transactions GROUP BY category'
    )
    # Execute query and return a cursor pointing to the result set.
    # rows is a set of tuples: [ ("food", 120), ("rent", 1000), ("entertainment", 60) ]
    # Fetch all rows from the query result as a list of tuples.
    rows = data.fetchall()
    result = {}
    # Iterate through each row in the query result.
    for row in rows:
        # Each row is a tuple: (category, total_amount)
        result[row[0]] = row[1]
        # Map category (row[0]) to total amount (row[1]) in result dictionary.
    con.close()
    return jsonify(result)    
    

# Database connection function.
def get_db_connection():
   con = sqlite3.connect("finance.db")
   # Unused in this version.
   # con.row_factory = sqlite3.Row
   return con

# Setup for Database Structure. Create table for transactions if one does not already exist.
def init_db():
    # Opens a connection to the database, if file doesn't exist SQLite creates it.
    con = sqlite3.connect("finance.db")
    cursor = con.cursor()
    # Table created with schema (id, amount, category, transactionType) if it does not already exist.
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS transactions(
                       id INTEGER PRIMARY KEY,
                       amount REAL,
                       category TEXT,
                       transactionType TEXT
                    )
                """)
    con.commit()
    con.close()


if __name__ == "__main__":
    init_db()
    app.run(debug=False, use_reloader=False)
