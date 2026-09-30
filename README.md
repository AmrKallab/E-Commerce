# E-Commerce Backend API

A RESTful e-commerce backend built with Django REST Framework, PostgreSQL, and JWT authentication.

Products, categories, shopping carts, shipping addresses, checkout, inventory, and order management—organized as a modular Django backend with transactional order processing and role-based API access.

---

## Overview

E-Commerce Backend API provides the core backend workflows required by an online store.

The system covers:

- User registration and JWT authentication
- Product and category management
- Customer shopping carts
- Shipping address management
- Order creation and history
- Inventory validation and stock updates
- Cash on delivery and payment-state modeling
- Administrative order management
- Controlled order-status transitions

The application is structured as a modular Django monolith. Each business area is isolated in its own Django application while sharing a single PostgreSQL database and REST API boundary.

---

## Core capabilities

| Capability | What it provides |
| --- | --- |
| **Identity & access** | User registration, JWT login, token refresh, authenticated user access, and protected endpoints |
| **Product catalog** | Categories, active products, pricing, stock tracking, and administrator-controlled catalog management |
| **Shopping cart** | Per-user carts, item addition, quantity updates, removal, calculated subtotals, and cart totals |
| **Shipping addresses** | Customer-owned shipping addresses with create, retrieve, update, and delete operations |
| **Checkout** | Shipping validation, cart validation, stock checks, order creation, inventory updates, and cart cleanup |
| **Order management** | Customer order history, order details, payment state, and administrative order access |
| **Order lifecycle** | Explicit order states with controlled transitions from creation through fulfillment |
| **Data integrity** | Atomic checkout operations, ownership checks, relational constraints, and server-side validation |

---

## Architecture

The backend follows a modular monolithic architecture built around Django applications.

Each application owns a specific business domain while Django REST Framework provides the common HTTP API layer.

```text
                         HTTP / JSON
                             │
                             ▼
                ┌─────────────────────────┐
                │ Django REST Framework   │
                │ Authentication · APIView│
                │ Permissions · Validation│
                └────────────┬────────────┘
                             │
              ┌──────────────┼───────────────┐
              │              │               │
              ▼              ▼               ▼
          Accounts        Products          Cart
              │              │               │
              └──────────────┼───────────────┘
                             │
                     ┌───────┴────────┐
                     ▼                ▼
                  Shipping          Orders
                     │                │
                     └───────┬────────┘
                             ▼
                       Django ORM
                             │
                             ▼
                        PostgreSQL
```

The domains are separated into:

- `accounts` — registration, authentication, and user endpoints
- `products` — product and category management
- `cart` — customer carts and cart items
- `shipping` — customer shipping addresses
- `orders` — checkout, order history, payment state, and order lifecycle
- `core` — project configuration and top-level routing

This keeps domain responsibilities separated without introducing the operational complexity of independently deployed services.

---

## Engineering highlights

| Design choice | Why it matters |
| --- | --- |
| **Modular Django applications** | Accounts, products, cart, shipping, and orders remain separated by business responsibility |
| **Transactional checkout** | Order creation, inventory updates, and cart cleanup execute as one database transaction |
| **Server-side ownership checks** | User-specific resources are resolved against the authenticated user rather than trusting client-provided ownership |
| **Role-based catalog access** | Product and category reads remain public while modifications are restricted to administrators |
| **Relational domain model** | Foreign keys and uniqueness constraints represent ownership and relationships directly in PostgreSQL |
| **Decimal pricing** | Monetary values use decimal storage rather than floating-point representation |
| **Order-item price snapshots** | Order items store the purchase price instead of depending only on the product's current price |
| **Explicit order state model** | Order progression is represented using defined states rather than arbitrary status values |
| **Environment-based configuration** | Database credentials and Django configuration are kept outside source code through environment variables |

---

## Checkout lifecycle

Checkout coordinates several domains and database changes in a single workflow.

```text
1. Authenticated customer submits checkout
                         │
2. Shipping address ownership is verified
                         │
3. Payment method is validated
                         │
4. Customer cart is loaded
                         │
5. Empty-cart validation is performed
                         │
6. Product stock is checked
                         │
7. Order and order items are created
                         │
8. Product inventory is reduced
                         │
9. Final order total is calculated
                         │
10. Cart items are cleared
                         │
11. Created order is returned
```

The write operations are executed inside `transaction.atomic()` so checkout is treated as one database operation rather than a collection of unrelated updates.

If checkout cannot be completed, its database changes can be rolled back instead of leaving a partially created order.

---

## Order lifecycle

Orders use explicit states to represent fulfillment progress.

```text
PENDING
   │
   ├──────────────► CANCELLED
   │
   ▼
CONFIRMED
   │
   ├──────────────► CANCELLED
   │
   ▼
PROCESSING
   │
   ├──────────────► CANCELLED
   │
   ▼
SHIPPED
   │
   ▼
DELIVERED
```

`DELIVERED` and `CANCELLED` are terminal states.

Administrative order endpoints are separated from customer endpoints and protected with administrator permissions.

---

## Domain model

The main entities and relationships are:

```text
User
 │
 ├──── 1:1 ──── Cart
 │                │
 │                └──── 1:N ──── CartItem
 │                                │
 │                                ▼
 │                             Product
 │                                │
 │                                └──── N:1 ──── Category
 │
 ├──── 1:N ──── ShippingAddress
 │
 └──── 1:N ──── Order
                  │
                  ├──── N:1 ──── ShippingAddress
                  │
                  └──── 1:N ──── OrderItem
                                   │
                                   ▼
                                Product
```

A cart item is unique for each cart/product combination, preventing the same product from being represented by multiple independent rows inside one cart.

Order items preserve the product name, quantity, and purchase price required to represent an order independently from future catalog changes.

---

## API surface

### Accounts

```text
POST   /api/accounts/register
POST   /api/accounts/login
POST   /api/accounts/token/refresh
GET    /api/accounts/me
```

### Products & categories

```text
GET    /api/products/categories
POST   /api/products/categories

GET    /api/products/categories/<id>
PUT    /api/products/categories/<id>
PATCH  /api/products/categories/<id>
DELETE /api/products/categories/<id>

GET    /api/products/products
POST   /api/products/products

GET    /api/products/products/<id>
PUT    /api/products/products/<id>
PATCH  /api/products/products/<id>
DELETE /api/products/products/<id>
```

Catalog reads are publicly accessible. Write operations require administrator privileges.

### Cart

```text
GET    /api/cart/
POST   /api/cart/add/
PATCH  /api/cart/items/<id>/
DELETE /api/cart/items/<id>/
DELETE /api/cart/clear/
```

Cart operations require authentication and operate on the current user's cart.

### Shipping

```text
GET    /api/shipping/addresses/
POST   /api/shipping/addresses/

GET    /api/shipping/addresses/<id>/
PUT    /api/shipping/addresses/<id>/
PATCH  /api/shipping/addresses/<id>/
DELETE /api/shipping/addresses/<id>/
```

Shipping addresses are scoped to their owning user.

### Orders

```text
POST   /api/orders/create
GET    /api/orders/
GET    /api/orders/<id>
```

### Administration

```text
GET    /api/orders/admin
PATCH  /api/orders/admin/<id>/status
```

Administrative order endpoints require staff privileges.

---

## Authentication and access control

The API uses `djangorestframework-simplejwt` for JWT authentication.

```text
Client
   │
   │ username + password
   ▼
POST /api/accounts/login
   │
   ├── access token
   └── refresh token
           │
           ▼
Authorization: Bearer <access_token>
           │
           ▼
Protected API
```

The authorization model distinguishes between public, authenticated, and administrator operations.

| Resource | Read | Write |
| --- | --- | --- |
| Products | Public | Admin |
| Categories | Public | Admin |
| Cart | Owner | Owner |
| Shipping addresses | Owner | Owner |
| Customer orders | Owner | Checkout flow |
| Administrative orders | Admin | Admin |

Ownership-sensitive queries use the authenticated user to prevent access to another customer's cart, shipping addresses, or orders.

---

## Payment model

Orders separate the selected payment method from payment state.

Supported payment methods in the current domain model include:

```text
CASH_ON_DELIVERY
STRIPE
```

Payment state is represented independently:

```text
UNPAID
PAID
FAILED
REFUNDED
```

This separation allows order fulfillment and payment processing to evolve independently.

The current project models Stripe as a payment method; external Stripe payment processing is not yet integrated.

---

## Technology stack

### Backend

- Python
- Django 6
- Django REST Framework
- Simple JWT
- python-decouple

### Database

- PostgreSQL
- Django ORM
- psycopg2

### Development

- Git
- Postman

---

## Repository structure

```text
.
├── accounts/
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── products/
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── cart/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── shipping/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── orders/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── core/
│   ├── settings.py
│   └── urls.py
│
├── .env.example
├── manage.py
└── requirements.txt
```

---

## Local setup

### Prerequisites

- Python
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/AmrKallab/E-Commerce.git
cd E-Commerce
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare environment configuration

Create a `.env` file from `.env.example`:

```env
SECRET_KEY=
DEBUG=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

Use development credentials locally and keep real secrets outside version control.

### 5. Prepare PostgreSQL

Create the database configured in `.env`, then apply the Django migrations:

```bash
python manage.py migrate
```

### 6. Create an administrator

```bash
python manage.py createsuperuser
```

### 7. Start the API

```bash
python manage.py runserver
```

The development API is available at:

```text
http://127.0.0.1:8000/
```

---


## Repository

https://github.com/AmrKallab/E-Commerce
