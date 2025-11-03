# Context Managers and Asynchronous Programming in Python

This project demonstrates advanced Python techniques for managing database connections and executing queries using context managers and asynchronous programming.

## Prerequisites

Install the required package for asynchronous SQLite operations:

```bash
pip install aiosqlite
```

## Setup

1. Run the database setup script:
```bash
python setup_database.py
```

2. Run individual task files:
```bash
python 0-databaseconnection.py
python 1-execute.py
python 3-concurrent.py
```

## Tasks

### Task 0: Custom Class-Based Context Manager
- **File**: `0-databaseconnection.py`
- **Description**: Class-based context manager for database connections using `__enter__` and `__exit__` methods

### Task 1: Reusable Query Context Manager
- **File**: `1-execute.py`
- **Description**: Context manager that takes a query as input and executes it, managing both connection and query execution

### Task 2: Concurrent Asynchronous Database Queries
- **File**: `3-concurrent.py`
- **Description**: Run multiple database queries concurrently using `asyncio.gather()` and `aiosqlite`

## Key Concepts

- **Context Managers**: Ensure proper resource acquisition and release
- **Database Connection Management**: Prevent resource leaks
- **Asynchronous Programming**: Non-blocking database operations
- **Concurrent Execution**: Multiple operations running simultaneously

## Real-World Applications

- Web application backends
- Data processing pipelines
- Analytics dashboards
- Microservices architecture
- Automated testing
