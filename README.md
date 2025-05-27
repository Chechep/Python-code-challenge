# Python Magazine Publishing App

A simple command-line Python app for managing authors, articles, and magazines using SQLite and raw SQL. Built for educational purposes, emphasizing OOP, database interactions, and clean architecture.

## Project Structure

├── lib/ # Main code directory
│ ├── models/ # Model classes
│ │ ├── __init__.py # Makes models a package
│ │ ├── author.py # Author class with SQL methods
│ │ ├── article.py # Article class with SQL methods
│ │ └── magazine.py # Magazine class with SQL methods
│ ├── db/ # Database components
│ │ ├── __init__.py # Makes db a package
│ │ ├── connection.py # Database connection setup
│ │ ├── seed.py # Seed data for testing
│ │ └── schema.sql # SQL schema definitions
│ ├── controllers/ # Optional: Business logic
│ │ └── __init__.py # Makes controllers a package
│ ├── debug.py # Interactive debugging
│ └── __init__.py # Makes lib a package
├── tests/ # Test directory
│ ├── __init__.py # Makes tests a package
│ ├── test_author.py # Tests for Author class
│ ├── test_article.py # Tests for Article class
│ └── test_magazine.py # Tests for Magazine class
├── scripts/ # Helper scripts
│ ├── setup_db.py # Script to set up the database
│ └── run_queries.py # Script to run example queries
└── README.md # Project documentation

---

## 🚀 Features

- Create and manage `Authors`, `Articles`, and `Magazines`
- Define relationships between them using foreign keys
- Raw SQL queries for full control and learning
- Complex queries like:
  - Top contributing author
  - All authors for a magazine
  - Magazines with articles from multiple authors
  - Article counts per magazine
- Test coverage with `unittest`

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone git@github.com:Chechep/Python-code-challenge.git
cd Python-code-challenge
```

### 2. Running test

```bash
pytest
```
