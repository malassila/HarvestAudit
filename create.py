import hashlib
import mysql.connector
mysql_host = '192.168.1.156'
mysql_database = 'sellercloud'
mysql_user = 'python'
mysql_password = 'ghXryPCSP2022!'
# Get the plain text password from the user
password = 'pcspuser'

# Hash the password
hashed_password = hashlib.sha256(password.encode()).hexdigest()
# Connect to the database
connection = mysql.connector.connect(host=mysql_host,
                                    port=3306,
                                    database=mysql_database,
                                    user=mysql_user,
                                    password=mysql_password)

# Create a cursor object to interact with the database
cursor = connection.cursor()
# Insert the username and hashed password into the database
cursor.execute("INSERT INTO sellercloud.users (username, password, is_admin) VALUES (%s, %s, %s)", (username, hashed_password, is_admin))
connection.commit()