# Personal Finance Tracking API

> Built as part of my effort to strengthen backend engineering fundamentals and reduce reliance on AI by implementing core concepts from scratch.

A simple RESTful API built with Flask that allows users to create, retrieve, and delete financial transactions.

## Features

- Create a transaction (`POST /transactions`)
- Retrieve all transactions (`GET /transactions`)
- Retrieve a transaction by ID (`GET /transactions/<id>`)
- Delete a transaction by ID (`DELETE /transactions/<id>`)
- In-memory data storage for quick prototyping

## Tech Stack

- Python
- Flask
- REST API design
- JSON request/response handling

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/sirmonsoon/personal-finance-api.git
cd personal-finance-api
