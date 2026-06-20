# E-Commerce Backend API

A RESTful backend API for an e-commerce platform built with Django REST Framework and PostgreSQL. It provides secure JWT authentication, product and category management, shopping cart functionality, order processing, and role-based access control for administrators and customers.

The project was developed to practice building scalable backend applications while following RESTful API principles and clean backend architecture.

## Features

- Secure JWT authentication
- Product management
- Category management
- Shopping cart management
- Order processing
- Automatic stock updates
- Role-based access control
- RESTful API design

## Tech Stack

- Python
- Django
- Django REST Framework (DRF)
- PostgreSQL
- JWT Authentication

## Architecture

                Client
                   │
                   ▼
          JWT Authentication
                   │
                   ▼
        Django REST Framework
                   │
     ┌────────┬─────────┬────────┐
     │        │         │        │
     ▼        ▼         ▼        ▼
 Accounts Products   Cart    Orders
                   │
                   ▼
              PostgreSQL

Client requests are authenticated using JWT and routed through the Django REST Framework application. Each module handles its own business logic and interacts with the PostgreSQL database using Django ORM