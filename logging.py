import mysql.connector
from datetime import datetime

mysql_host = '192.168.1.156'
mysql_database = 'logs'
mysql_user = 'python'
mysql_password = 'ghXryPCSP2022!'

def log_print(user, sku, chassis):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        connection = mysql.connector.connect(host=mysql_host, port=3306, database=mysql_database, user=mysql_user, password=mysql_password)
        
        cursor = connection.cursor()
        
        query = "INSERT INTO `print_log` (`user`, `sku`, `chassis`, `date_time`) VALUES (%s, %s, %s, %s)"
        
        cursor.execute(query, (user, timestamp, sku, chassis, timestamp))
        
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def log_add_remove_event(user, sku, chassis):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        connection = mysql.connector.connect(host=mysql_host, port=3306, database=mysql_database, user=mysql_user, password=mysql_password)
        
        cursor = connection.cursor()
        
        query = "INSERT INTO `add_remove_log` (`user`, `sku`, `chassis`, `date_time`) VALUES (%s, %s, %s, %s)"
        
        cursor.execute(query, (user, sku, chassis, timestamp))
        
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def log_login_event(user):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        connection = mysql.connector.connect(host=mysql_host, port=3306, database=mysql_database, user=mysql_user, password=mysql_password)
        
        cursor = connection.cursor()
        
        query = "INSERT INTO `add_remove_log` (`user`, `date_time`) VALUES (%s, %s)"
        
        cursor.execute(query, (user, timestamp))
        
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
