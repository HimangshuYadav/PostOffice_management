import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="root",passwd="")
cursor=mydb.cursor()
cursor.execute("create database postoffice; use postoffice;")
cursor.execute("create table Customer_details(UID int primary key,password varchar(30),name varchar(20),email varchar(21),history varchar(200));")
cursor.execute("create table parcel_details(PID int primary key,in_transit boolean default False, out_for_delivery boolean default False,delivered boolean default False,returned boolean default False, sender_add varchar(20), reciever_add varchar(20));")
cursor.execute("create table Staff_details(SID int primary key,password varchar(30),name varchar(20),email varchar(21));")

