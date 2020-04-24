## Code handling good, but for auto increment part will be tested in next version
import ibm_db
import json
import mysql.connector

#import MySQLdb as mariadb

# some JSON:
x =  '{ "username":"dinga", "req_text":"I need to boats for moving to relief camp", "Latitude":22.2113, "longitude":43.1224, "phone":9845420420, "req_type":"P3"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
#print(y["age"])
#print(y["username"])
#print(y["req_text"])

user_name = y["username"]
request_content = y["req_text"]
latitude = y["Latitude"]
longitude = y["longitude"]
phone = y["phone"]
req_type = y["req_type"]

print(user_name)
print(request_content)
print(latitude)
print(longitude)
print(phone)
print(req_type)

#Replace the placeholder values with your actual Db2 hostname, username, and password:
dsn_hostname =  "dashdb-txn-sbox-yp-lon02-04.services.eu-gb.bluemix.net"
dsn_uid = "xsg48981"
dsn_pwd = "lm0d2svj^v2fsn15"

dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"            # e.g. "BLUDB"
dsn_port = "50000"                # e.g. "50000" 
dsn_protocol = "TCPIP"            # i.e. "TCPIP"

#Create database connection
#DO NOT MODIFY THIS CELL. Just RUN it with Shift + Enter
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)

try:
    conn = ibm_db.connect(dsn, "", "")
    print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)
 
except:
    print ("Unable to connect: ", ibm_db.conn_errormsg() )
    
print("success");

#Construct the query that retrieves all rows from the REQUESTER table
##insert = "insert into requester (USER_NAME, REQ_TEXT, LATITUDE, LONGITUDE, PHONE, REQ_TYPE) VALUES ( 'abanoopb', 'Please provide ambulance service', 21.2212, 23.1234, 8951523243, 'P1')"
##ibm_db.exec_immediate(conn,insert)

insert = "insert into requester (USER_NAME, REQ_TEXT, LATITUDE, LONGITUDE, PHONE, REQ_TYPE) VALUES (?,?,?,?,?,?);"
#params="( 'abanoopb', 'Please provide ambulance service', 21.2212, 23.1234, 8951523243, 'P1')"
stmt = ibm_db.prepare(conn, insert)

ibm_db.bind_param(stmt, 1, user_name)
ibm_db.bind_param(stmt, 2, request_content)
ibm_db.bind_param(stmt, 3, latitude)
ibm_db.bind_param(stmt, 4, longitude)
ibm_db.bind_param(stmt, 5, phone)
ibm_db.bind_param(stmt, 6, req_type)
ibm_db.execute(stmt)

#Construct the query that retrieves unique id generated from the REQUESTER table    
stmt = ibm_db.exec_immediate(conn, "SELECT unique SYSIBM.IDENTITY_VAL_LOCAL() AS id FROM requester")
result = ibm_db.fetch_both(stmt)
print("Number of affected rows: ", result[0]);  
    
ibm_db.close(conn);
print("success 2");