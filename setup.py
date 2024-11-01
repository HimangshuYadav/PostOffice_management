import mysql.connector

'''
Tables to be made:
Customer details
UID(PK),name,email,password,history

staff details
SID(PK),name,SEmail,password

Admin details
AID(PK),name,password

parcel details
parcel_ID(PK),user,in_transit, out_for_delivery,delivered,returned,to,from

Complaint
CID(PK),issuer_name,issuer_ID,complaint,date of complaint

Finance

'''

mydb=mysql.connector.connect(host="localhost",user="root",passwd="")
cursor=mydb.cursor()
cursor.execute("create database postoffice; use postoffice;")
cursor.execute("create table Customer_details(UID int primary key,password varchar(30),name varchar(20),email varchar(21),history varchar(200));")
cursor.execute("create table parcel_details(PID int primary key,in_transit boolean default False, out_for_delivery boolean default False,delivered boolean default False,returned boolean default False, sender_add varchar(20), reciever_add varchar(20));")
cursor.execute("create table Staff_details(SID int primary key,password varchar(30),name varchar(20),email varchar(21));")
# cursor.execute("create table complaint(CID int primary key,issuer_name varchar(20),issuer_ID int,complaint varchar(240),date_of_complaint date);")
cursor.execute("create table complaint(CID int primary key,complainant_name varchar(20),complainant _ID int,complaint varchar(240),date_of_complaint date);")

