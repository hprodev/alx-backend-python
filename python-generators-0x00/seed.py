import mysql.connector
import csv
import requests
import io

# S3 URL for the CSV file
CSV_URL = "https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2024/12/3888260f107e3701e3cd81af49ef997cf70b6395.csv"


# Function to connect to the MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# Function to create the database ALX_prodev
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    print("Database ALX_prodev created or already exists.")
    cursor.close()


# Function to connect to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Change this to your MySQL username
            password="root",  # Change this to your MySQL password
            database="ALX_prodev",
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# Function to create the user_data table
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,0) NOT NULL
    );
    """
    )
    print("Table user_data created successfully")
    cursor.close()


# Function to insert data directly from S3 CSV
def insert_data_from_s3(connection):
    cursor = connection.cursor()
    print("Downloading CSV from S3...")
    response = requests.get(CSV_URL)
    if response.status_code == 200:
        csv_file = io.StringIO(response.text)
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header
        for row in csv_reader:
            name, email, age = row
            cursor.execute(
                """
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (UUID(), %s, %s, %s);
                """,
                (name, email, age),
            )
        connection.commit()
        print("Data inserted from S3 CSV.")
    else:
        print("Failed to download CSV from S3.")
    cursor.close()
