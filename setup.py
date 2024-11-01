import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="root",passwd="")
cursor=mydb.cursor()
cursor.execute("create database postoffice; use postoffice;")
cursor.execute("create table Customer_details(UID int primary key,password varchar(30),name varchar(20),email varchar(21),history(200))")
cursor.execute("create table parcel_details(PID int primary key,user int,in_transit boolean default False, out_for_delivery boolean default False,delivered boolean default False,returned boolean default False);)")


