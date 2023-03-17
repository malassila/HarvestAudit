import mysql.connector
from datetime import datetime

mysql_host = '192.168.1.160'
mysql_database = 'sellercloud'
mysql_user = 'matt'
mysql_password = 'ghXryPCSP2022!'


log_path = "C:\\HarvestAudit\\log.txt"

# Define a function to log messages
def log_message(message, log_type="info"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_path, "a") as log_file:
        log_file.write(f"{timestamp} [{log_type.upper()}] {message}\n")

def get_connection():
    try:
        return mysql.connector.connect(
            host=mysql_host,
            database=mysql_database,
            user=mysql_user,
            password=mysql_password
        )
    except mysql.connector.Error as error:
        log_message(f'Error while connecting to MySQL: {error}')
        log_message(f'Host: {mysql_host}')
        log_message(f'Database: {mysql_database}')
        return None

    
def query_database(query_string):
    try:
        connection = get_connection()
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        cursor.execute(query_string)
        result = cursor.fetchall()
        count = len(result)
        
        log_message(f'Query: {query_string}')
        log_message(f'Result count: {count}')
        return result
    except mysql.connector.Error as error:
        log_message(f'Error while connecting to MySQL: {error}')
        log_message(f'Query: {query_string}')
    finally:
        cursor.close()
        connection.close()
    return result