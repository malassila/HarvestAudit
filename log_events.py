import mysql.connector
from datetime import datetime
import socket
import traceback

mysql_host = '192.168.1.156'
mysql_database = 'logs'
mysql_user = 'python'
mysql_password = 'ghXryPCSP2022!'


def log_print(log_entries):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        connection = mysql.connector.connect(
            host=mysql_host,
            port=3306,
            database=mysql_database,
            user=mysql_user,
            password=mysql_password
        )
        cursor = connection.cursor()

        query = "INSERT INTO `print_log` (`user`, `sku`, `chassis`, `date_time`) VALUES (%s, %s, %s, %s)"
        values = [(entry[0], entry[1], entry[2], timestamp) for entry in log_entries]

        cursor.executemany(query, values)

        connection.commit()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def log_add_remove_event(events):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        connection = mysql.connector.connect(host=mysql_host, port=3306, database=mysql_database, user=mysql_user, password=mysql_password)
        
        cursor = connection.cursor()
        
        query = "INSERT INTO `add_remove_log` (`user`, `sku`, `chassis`, `event_type`, `date_time`) VALUES (%s, %s, %s, %s, %s)"
        
        values_list = []
        for event in events:
            values_list.append((event[0], event[1], event[2], event[3], timestamp))

        cursor.executemany(query, values_list)
        
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
        
        # Get the ip address of the current machine
        ip = socket.gethostbyname(socket.gethostname())
        
        connection = mysql.connector.connect(host=mysql_host, port=3306, database=mysql_database, user=mysql_user, password=mysql_password)
        
        cursor = connection.cursor()
        
        query = "INSERT INTO `login_log` (`user`, `ip_address`, `date_time`) VALUES (%s, %s, %s)"
        
        cursor.execute(query, (user, ip, timestamp))
        
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
