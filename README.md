# Personal Finance Tracking API

> Built as part of my effort to strengthen backend engineering fundamentals and reduce reliance on AI by implementing core concepts from scratch.

A simple RESTful API built with Flask that allows users to create, retrieve, and delete financial transactions.

## Features

- Create transactions (POST /transactions)
- Get all transactions (GET /transactions)
- Get transaction by ID (GET /transactions/<id>)
- Update transaction (PUT /transactions/<id>)
- Delete transaction (DELETE /transactions/<id>)

## Tech Stack

- Python
- Flask
- REST API design
- SQLite
- JSON request/response handling

## Setup Instructions

## How to Run
1. Clone repo
2. Install dependencies
3. Run app

## Example Request
POST /transactions
{
  "amount": 50,
  "category": "food",
  "transactionType": "expense"
}
