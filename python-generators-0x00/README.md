# Database Seed Utility

## Overview

The `seed.py` script provides a complete solution for setting up and populating a MySQL database with user data. It handles everything from establishing database connections to importing data from a remote CSV file hosted on Amazon S3.

## Key Functionality

### Database Connection & Setup

- Establishes connections to the MySQL server running on localhost
- Creates the `ALX_prodev` database if it doesn't already exist
- Sets up proper user authentication with configurable credentials

### Table Creation

Creates a structured `user_data` table with the following fields:

- `user_id`: CHAR(36) - Unique identifier (Primary Key)
- `name`: VARCHAR(255) - User's full name
- `email`: VARCHAR(255) - User's email address
- `age`: DECIMAL(3,0) - User's age

### Data Population

- Fetches user data directly from an Amazon S3 bucket
- Processes and imports CSV data without requiring local file downloads
- Generates unique UUIDs for each record automatically
- Uses `INSERT IGNORE` to prevent duplicate entries

## Functions

### `connect_db()`

Establishes the initial connection to the MySQL server, with proper error handling.

### `create_database(connection)`

Creates the `ALX_prodev` database if it doesn't exist.

### `connect_to_prodev()`

Establishes a connection specifically to the `ALX_prodev` database.

### `create_table(connection)`

Sets up the `user_data` table with the appropriate schema.

### `insert_data_from_s3(connection)`

Fetches and processes the CSV file from the S3 URL, inserting data into the database.

## Data Source

The script retrieves data from:

```web


https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2024/12/3888260f107e3701e3cd81af49ef997cf70b6395.csv
```

## Usage

Simply import and call the appropriate functions from this module:

```python
import seed

# To establish a connection to the ALX_prodev database
connection = seed.connect_to_prodev()

# To perform the entire setup process
connection = seed.connect_db()
seed.create_database(connection)
connection = seed.connect_to_prodev()
seed.create_table(connection)
seed.insert_data_from_s3(connection)
```
