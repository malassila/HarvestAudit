import mysql.connector

mysql_host = 'localhost'
mysql_database = 'sellercloud'
mysql_user = 'matt'
mysql_password = 'ghXryPCSP2022!'


def get_connection():
    return mysql.connector.connect(
        host=mysql_host,
        database=mysql_database,
        user=mysql_user,
        password=mysql_password
    )
    
def query_database(query_string):
    try:
        connection = get_connection()
        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        cursor.execute(query_string)
        result = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    return result