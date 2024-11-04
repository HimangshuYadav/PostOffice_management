import mysql.connector as con

mydb=con.connect(host="localhost",user="root",passwd="uhsgnamih")
cursor=mydb.cursor()
cursor.execute("use postoffice;")
