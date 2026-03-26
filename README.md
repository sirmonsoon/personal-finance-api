[Built as part of my effort to strengthen backend engineering fundamentals and reduce reliance on AI by implementing core concepts from scratch]

Personal Finance Tracking API
  Desc: A simple RESTful API built with Flask that allows users to create, retrieve, and delete financial transactions.

  Features:
    - Create a transaction (POST)
    - Retrieve all transactions (GET)
    - Retrieve a transaction by ID (GET)
    - Delete a transaction (DELETE)
    - In-memory data storage (Database not yet implemented)

  Tech Stack:
    - Python
    - Flask
    - REST API design
    - JSON handling

Setup Instructions:
  1. Clone the repo:
       git clone <your-repo-url>
       cd personal-finance-api
  2. Create virtual environment:
       python -m venv venv
  3. Activate it:
       venv\Scripts\activate -> Windows
       source venv/bin/activate -> Mac/Linux
  4. Install dependencies:
       pip install -r requirements.txt
  5. Run the server:
       python app.py
       Server runs at http://127.0.0.1:5000/

API Endpoints
  + Create Transaction
      POST /transactions
        Request Body:
        {
          "amount": 25,
          "category": "gym",
          "transactionType": "expense"
        }
        Reponse:
        {
          "id": 1,
          "amount": 25,
          "category": "gym",
          "transactionType": "expense"
        }
  + Get All Transactions
      GET /transactions
        Response:
        [
          {
            "id": 1,
            "amount": 25,
            "category": "gym",
            "transactionType": "expense"
          }
        ]
  + Get Transaction by ID
      Example:
        Get /transactions/1
  + Delete Transaction
      DELETE /transactions/<id>
        Response:
          {
            "message": "Successfully deleted"
          }

What I learned / Key Takeaways:
  - Building RESTful APIs with Flask
  - Handling HTTP methods (GET, POST, DELETE)
  - Working with JSON request/response
  - Debugging environment issues (Flask + OneDrive)
  - Implementing core backend logic and data flow
Future Improvements:
  - Add PUT endpoints (to update transactions)
  - Add database (SQLite / PostgreSQL)
  - Add authentication (user accounts)
  - Add categories and budgeting features
  - Improve error handling and validation
      

  
