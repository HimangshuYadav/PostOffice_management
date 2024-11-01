import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="root",passwd="uhsgnamih")
cursor=mydb.cursor()
cursor.execute("use postoffice_test;")
To=input("Enter Recievers Address :")
From=input("Enter Senders Address :")
cursor.execute("select PID from parcel_details order by PID desc;")
last_PID=cursor.fetchone()[0]
print(last_PID)
current_PID=last_PID+1
print(current_PID)
cursor.execute("insert into parcel_details values(%s,false,false,false,false,%s,%s);",(current_PID,From,To))
        

