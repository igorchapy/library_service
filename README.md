# REST_practice
# Library Management System API

## Overview

This project is a **Library Management System API** built with a microservices architecture, designed to manage library resources, users, borrowings, notifications, and payments. The backend services expose RESTful APIs for operations like managing books, user authentication, borrowing books, processing payments via Stripe, and sending notifications via Telegram.

---

## Features

### Books Service
- Manage library books (CRUD operations)
- Track book inventory and daily rental fee
- API endpoints:
  - `POST /books/` — Add a new book
  - `GET /books/` — List all books
  - `GET /books/<id>/` — Retrieve book details
  - `PUT/PATCH /books/<id>/` — Update book info and inventory
  - `DELETE /books/<id>/` — Delete a book

### Users Service
- User registration and authentication
- JWT token-based authentication with refresh support
- API endpoints:
  - `POST /users/` — Register new user
  - `POST /users/token/` — Obtain JWT access and refresh tokens
  - `POST /users/token/refresh/` — Refresh JWT token
  - `GET /users/me/` — Get current user profile
  - `PUT/PATCH /users/me/` — Update user profile

### Borrowings Service
- Manage book borrowings and returns
- Automatically update book inventory on borrowing and return
- API endpoints:
  - `POST /borrowings/` — Create new borrowing (inventory -1)
  - `GET /borrowings/?user_id=&is_active=` — Get borrowings by user and active status
  - `GET /borrowings/<id>/` — Get borrowing details
  - `POST /borrowings/<id>/return/` — Return book (inventory +1)

### Notifications Service (Telegram)
- Sends notifications to library administrators for:
  - New borrowings
  - Overdue borrowings
  - Successful payments
- Runs asynchronously using Django Q or Celery
- Uses Telegram API to interact with chats and bots

### Payments Service (Stripe)
- Handles payments for borrowings and fines via Stripe
- Interacts with Stripe API using the `stripe` Python package
- API endpoints:
  - `GET /success/` — Stripe payment success callback
  - `GET /cancel/` — Stripe payment cancellation callback

---

## Data Models

### Book
- **Title:** string
- **Author:** string
- **Cover:** enum (`HARD` | `SOFT`)
- **Inventory:** positive integer (available copies)
- **Daily fee:** decimal (in USD)

### User
- **Email:** string
- **First name:** string
- **Last name:** string
- **Password:** string (hashed)
- **Is staff:** boolean

### Borrowing
- **Borrow date:** date
- **Expected return date:** date
- **Actual return date:** date or null
- **Book id:** int (foreign key)
- **User id:** int (foreign key)

### Payment
- **Status:** enum (`PENDING` | `PAID`)
- **Type:** enum (`PAYMENT` | `FINE`)
- **Borrowing id:** int (foreign key)
- **Session url:** URL (Stripe payment session link)
- **Session id:** string (Stripe payment session id)
- **Money to pay:** decimal (in USD)

---

## Installation & Setup

### Requirements
- Python 3.10+
- PostgreSQL or other supported database
- Redis (for Celery or Django Q backend)
- Stripe account and API keys

- Telegram bot token and chat IDs
- Telegram bot 
