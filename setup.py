import subprocess

'''
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
'''
def setup():
    try:
        # Use pip to install packages from the requirements.txt file
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        print(f"Packages from {'requirements.txt'} have been installed successfully.")
    except subprocess.CalledProcessError:
        print("An error occurred while trying to install the packages.")
    except FileNotFoundError:
        print(f"{'requirements.txt'} not found. Please ensure the file exists.")
        
    import mysql.connector
    from colorama import Fore,Style


    mydb=mysql.connector.connect(host="localhost",user="root",passwd="")
    cursor=mydb.cursor()
    cursor.execute("create database if not exists postoffice;")
    cursor.execute("use postoffice;")
    cursor.execute("create table Customer_details(UID int primary key,password varchar(50),name varchar(50),email varchar(50));")
    cursor.execute("create table parcel_details(PID int primary key,in_transit boolean default False, out_for_delivery boolean default False,delivered boolean default False,returned boolean default False, sender_add varchar(20), reciever_add varchar(20));")
    cursor.execute("create table Staff_details(SID int primary key,password varchar(50),name varchar(50),email varchar(50));")
    cursor.execute("create table complaint(CID int primary key,complainant_name varchar(50),complainant_ID int,complaint varchar(254),date_of_complaint date);")
    cursor.execute("create table Admin_Details(AID int primary key,Admin_name varchar(50),Email varchar(50),password varchar(50));")
    cursor.execute("insert into admin_details values(1,'Himangshu','kuchbhi@indiapost.com','12345678');")
    mydb.commit()
    print(Fore.GREEN+"SetUp Successful"+Style.RESET_ALL)
    
if __name__=="__main__":
    setup()
