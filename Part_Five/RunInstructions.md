# How to Run - Bookstore/Library GUI (Part Five)

## Prerequisites
- PostgreSQL server running, with the `LibraryBookStore` database restored (from the Part Four backup or from the Part_One-Four SQL scripts run in order).
- Python 3.10+ installed.

## 1. Install dependencies
From the `Code` folder, run:
```bash
python -m pip install psycopg2-binary matplotlib numpy pillow
```

## 2. Configure the database connection
Open `Code/config.py` and make sure the connection details match your PostgreSQL server:
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'LibraryBookStore',
    'user': 'YOUR_USERNAME',
    'password': 'YOUR_PASSWORD'
}
```

## 3. Run the application
From the `Code` folder:
```bash
python main.py
```

The main menu window will open, with six categories: CRUD Table Management, Information Functions, Statistics, Queries, Procedures, and Main Programs. Every screen in the system is reachable from this main window.