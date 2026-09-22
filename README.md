# E-Commerce Backend API

## About
A production-style E-Commerce Backend API built using FastAPI and SQLAlchemy.

## Features

- User Registration & Login
- JWT Authentication
- Password Hashing
- Admin Authorization
- Product CRUD
- Product Image Upload
- Pagination
- Filtering
- Searching
- Sorting
- Shopping Cart
- Order Management
- Order Status Management
- SQLAlchemy Relationships
- Input Validation
- Error Handling
- Logging
- Pytest
- Docker
- Environment Variables

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT
- Pytest
- Docker

## API Documentation

Swagger:
`/docs`

ReDoc:
`/redoc`

## Health Check

`GET /health`

## Run Locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload