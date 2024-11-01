import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="root",passwd="uhsgnamih")
cursor=mydb.cursor()
cursor.execute("use postoffice_test;")
cursor.execute(f"select * from parcel_details where PID=1")
info=cursor.fetchone()
print(info)

