import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database configuration from .env
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

TABLES = [
    "mcq_options",
    "annotations",
    "mcqs",
    "topics",
    "chapters",
    "books"
]

def delete_all_tables():
    try:
        # Establish database connection
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Connected to the database.")
            cursor = connection.cursor()

            # Disable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            print("Foreign key checks disabled.")

            # Start transaction
            connection.start_transaction()
            try:
                # Truncate each table and reset auto-increment
                for table in TABLES:
                    cursor.execute(f"TRUNCATE TABLE {table};")
                    print(f"Table '{table}' truncated successfully.")

                # Commit transaction
                connection.commit()
                print("Transaction committed successfully.")

            except Error as e:
                # Rollback if any truncation fails
                connection.rollback()
                print(f"Error occurred during table truncation: {e}")
                print("Transaction rolled back.")

            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            print("Foreign key checks re-enabled.")

    except Error as e:
        print(f"Database connection error: {e}")
    
    finally:
        # Close cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    delete_all_tables()
