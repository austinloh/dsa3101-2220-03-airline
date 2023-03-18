import mysql.connector
from sshtunnel import SSHTunnelForwarder

#change aws ip address (current = 3.238.102.242), change path to pem file
tunnel = SSHTunnelForwarder(('3.238.102.242', 22), ssh_username='ubuntu', ssh_pkey='/Users/austinloh/Downloads/dsa3101-03.pem', remote_bind_address=('127.0.0.1', 3306))
tunnel.start()
conn = mysql.connector.connect(host='127.0.0.1', user='root', password='rootpw', port=tunnel.local_bind_port, use_pure=True, database='mydb')
cursor = conn.cursor()

#change SQL command
cursor.execute('SELECT * FROM flights LIMIT 1;') 
result = cursor.fetchall()
print(result)