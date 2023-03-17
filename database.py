import mysql.connector
from harvest_main import log_message, log_path

mysql_host = '192.168.1.160'
mysql_database = 'sellercloud'
mysql_user = 'matt'
mysql_password = 'ghXryPCSP2022!'


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
    except mysql.connector.Error as error:
        log_message(f'Error while connecting to MySQL: {error}')
        log_message(f'Query: {query_string}')
    finally:
        cursor.close()
        connection.close()
    return result