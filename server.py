import mysql.connector
from mysql.connector import Error
from datetime import datetime

def manage_numberplate_db(numberplate):
    """Connect to the MySQL database, create database, create table, insert number plate, and fetch data."""
    
    # Fixed connection parameters
    host = "127.0.0.1"
    user = "root"
    password = ""
    database = "numberplate"
    port = 3306
    
    connection = None
    try:
        # Step 1: Connect to MySQL Server
        print("Attempting to connect to MySQL Server...")
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        if connection.is_connected():
            print("Connection to MySQL Server successful")
            
            # Step 2: Create the database if it doesn't exist
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            print(f"Database '{database}' checked/created.")
            
            # Step 3: Connect to the specific database
            connection.database = database

            # Step 4: Create the new table 'numberplate'
            create_table_query = """
            CREATE TABLE IF NOT EXISTS numberplate (
                id INT AUTO_INCREMENT PRIMARY KEY,
                numberplate TEXT NOT NULL,
                entry_date DATE,
                entry_time TIME
            )
            """
            print("Creating table if not exists...")
            cursor.execute(create_table_query)
            connection.commit()  # Commit the table creation
            print("Table created successfully")

            # Step 5: Insert data into the 'numberplate' table
            insert_data_query = """
            INSERT INTO numberplate (numberplate, entry_date, entry_time)
            VALUES (%s, %s, %s)
            """
            current_date = datetime.now().date()  # Get current date
            current_time = datetime.now().time()  # Get current time
            data = (numberplate, current_date, current_time)  # Numberplate data
            
            print("Inserting data into the table...")
            cursor.execute(insert_data_query, data)
            connection.commit()  # Commit the data insertion
            print("Data inserted successfully")

            # Step 6: Retrieve and display data from the table
            fetch_data_query = "SELECT * FROM numberplate"
            print("Fetching data from the table...")
            cursor.execute(fetch_data_query)
            result = cursor.fetchall()
            for row in result:
                print(row)

    except Error as e:
        print(f"Error: '{e}'")
    
    finally:
        # Close the connection
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

