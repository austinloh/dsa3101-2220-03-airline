import mysql.connector
from sshtunnel import SSHTunnelForwarder

# port-forwarding
#change aws ip address (current = 50.19.153.183), change path to pem file
tunnel = SSHTunnelForwarder(('50.19.153.183', 22), ssh_username='ubuntu', ssh_pkey='./pem/dsa3101-03.pem', remote_bind_address=('127.0.0.1', 3306))
tunnel.start()
#print(tunnel.local_bind_port)

# connecting to SQL database
conn = mysql.connector.connect(host='127.0.0.1', user='root', password='rootpw', port=tunnel.local_bind_port, use_pure=True, database='mydb')
cursor = conn.cursor()

#change SQL command
cursor.execute('SHOW TABLES;') 
result = cursor.fetchall()
print(result)
#cursor.close()
#conn.close()