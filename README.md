# Python Generators - 0x00

## Project Overview

This project demonstrates advanced usage of Python generators to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations. The focus is on leveraging Python's `yield` keyword to implement generators that provide iterative access to data.

## Learning Objectives

- **Master Python Generators**: Create and utilize generators for iterative data processing
- **Handle Large Datasets**: Implement batch processing and lazy loading
- **Simulate Real-world Scenarios**: Develop solutions for live data updates
- **Optimize Performance**: Use generators for memory-efficient aggregate functions
- **Apply SQL Knowledge**: Integrate Python with databases for robust data management

## Requirements

- Python 3.x
- MySQL Server
- mysql-connector-python package
- Understanding of `yield` and generator functions
- SQL and database operations knowledge

## Project Structure

```
python-generators-0x00/
├── seed.py                 # Database setup and data seeding
├── 0-stream_users.py       # Stream users one by one
├── 1-batch_processing.py   # Batch processing with filtering
├── 2-lazy_paginate.py      # Lazy pagination implementation
├── 4-stream_ages.py        # Memory-efficient age aggregation
├── user_data.csv           # Sample data (required)
└── README.md               # This file
```

## Installation

### 1. Install MySQL Connector

```bash
pip install mysql-connector-python
```

### 2. Set Up MySQL Database

Update the MySQL connection credentials in all Python files:
- `host`: 'localhost'
- `user`: 'root'
- `password`: 'your_mysql_password'

### 3. Download Sample Data

Download the `user_data.csv` file and place it in the project directory.

## Usage

### Task 0: Database Setup and Seeding

```bash
./0-main.py
```

This script:
- Creates the `ALX_prodev` database
- Creates the `user_data` table with fields:
  - `user_id` (Primary Key, UUID, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Populates the table with data from `user_data.csv`

**Functions:**
- `connect_db()` - Connects to MySQL server
- `create_database(connection)` - Creates ALX_prodev database
- `connect_to_prodev()` - Connects to ALX_prodev database
- `create_table(connection)` - Creates user_data table
- `insert_data(connection, data)` - Inserts CSV data

### Task 1: Stream Users

```bash
./1-main.py
```

Streams rows from the database one by one using a generator.

**Function:**
- `stream_users()` - Generator that yields user dictionaries

**Key Features:**
- Memory-efficient iteration
- Single loop implementation
- Uses `yield` for lazy evaluation

### Task 2: Batch Processing

```bash
./2-main.py
```

Fetches and processes data in batches, filtering users over age 25.

**Functions:**
- `stream_users_in_batches(batch_size)` - Yields batches of users
- `batch_processing(batch_size)` - Processes and filters batches

**Key Features:**
- Maximum 3 loops
- Batch size customization
- Age filtering (> 25)

### Task 3: Lazy Pagination

```bash
./3-main.py
```

Implements lazy loading of paginated data.

**Functions:**
- `paginate_users(page_size, offset)` - Fetches a page of data
- `lazy_pagination(page_size)` - Generator for lazy page loading

**Key Features:**
- Single loop implementation
- On-demand page fetching
- Efficient memory usage

### Task 4: Memory-Efficient Aggregation

```bash
./4-stream_ages.py
```

Calculates average age without loading entire dataset into memory.

**Functions:**
- `stream_user_ages()` - Generator that yields ages
- `calculate_average_age()` - Computes average using generator

**Key Features:**
- Maximum 2 loops
- No SQL AVERAGE function
- Streaming computation

## Examples

### Streaming Users

```python
from itertools import islice

# Print first 6 users
for user in islice(stream_users(), 6):
    print(user)
```

### Batch Processing

```python
# Process users in batches of 50
batch_processing(50)
```

### Lazy Pagination

```python
# Paginate with 100 users per page
for page in lazy_pagination(100):
    for user in page:
        print(user)
```

### Average Age Calculation

```python
# Calculate average age
calculate_average_age()
# Output: Average age of users: 56.78
```

## Generator Benefits

1. **Memory Efficiency**: Only one item in memory at a time
2. **Lazy Evaluation**: Compute values only when needed
3. **Infinite Sequences**: Can represent infinite data streams
4. **Pipeline Processing**: Chain multiple generators together
5. **Improved Performance**: Reduced memory footprint for large datasets

## Database Schema

```sql
CREATE TABLE user_data (
    user_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL(3, 0) NOT NULL,
    INDEX idx_user_id (user_id)
);
```

## Testing

Each task includes a test script (`0-main.py`, `1-main.py`, etc.) that demonstrates the functionality.

To test individual components:

```bash
# Test database setup
python3 0-main.py

# Test streaming
python3 1-main.py

# Test batch processing
python3 2-main.py | head -n 5

# Test pagination
python3 3-main.py | head -n 7

# Test age aggregation
python3 4-stream_ages.py
```

## Best Practices

1. **Always close database connections** after use
2. **Use context managers** for resource management
3. **Handle exceptions** gracefully
4. **Use generators** for large datasets
5. **Optimize SQL queries** with proper indexing
6. **Validate input data** before processing
7. **Use prepared statements** to prevent SQL injection

## Troubleshooting

### MySQL Connection Error
```
Error connecting to MySQL: Access denied for user 'root'@'localhost'
```
**Solution**: Update the password in all Python files

### CSV File Not Found
```
FileNotFoundError: 'user_data.csv' not found
```
**Solution**: Ensure `user_data.csv` is in the project directory

### No Data Retrieved
```
No users found in database
```
**Solution**: Run `0-main.py` to seed the database first

## Performance Metrics

| Method | Memory Usage | Speed | Use Case |
|--------|--------------|-------|----------|
| List Loading | High | Fast | Small datasets |
| Generator | Low | Moderate | Large datasets |
| Batch Processing | Moderate | Fast | Bulk operations |
| Lazy Pagination | Low | Moderate | UI pagination |

## Author

**ALX Software Engineering Program**
- Project: Python Generators
- Weight: 1
- Deadline: November 3, 2025

## Repository

- **GitHub repository**: alx-backend-python
- **Directory**: python-generators-0x00

## License

This project is part of the ALX Software Engineering curriculum.

---

**Note**: Remember to request a manual QA review when you complete the project!
