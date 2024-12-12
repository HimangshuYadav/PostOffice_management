import subprocess
import pickle

def setup():
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        print(f"Packages from {'requirements.txt'} have been installed successfully.")
    except subprocess.CalledProcessError:
        print("An error occurred while trying to install the packages.")
    except FileNotFoundError:
        print(f"{'requirements.txt'} not found. Please ensure the file exists.")
        
    import mysql.connector
    from colorama import Fore,Style
    password=get_pass()
    mydb=mysql.connector.connect(host="localhost",user="root",passwd=password)
    cursor=mydb.cursor()
    cursor.execute("create database postoffice;")
    cursor.execute("use postoffice;")
    cursor.execute("create table Customer_details(UID int primary key,password varchar(50),name varchar(50),email varchar(50),dob date,address varchar(50),contact_number int);")
    cursor.execute("create table parcel_details(PID int primary key,in_transit boolean default False, out_for_delivery boolean default False,delivered boolean default False,returned boolean default False, sender_add varchar(20), reciever_add varchar(20));")
    cursor.execute("create table Staff_details(SID int primary key,name varchar(50),email varchar(50),password varchar(50),Designation varchar(15),Branch_loc varchar(25),DOJ date);")
    cursor.execute("create table complaint(CID int primary key,complainant_name varchar(50),complainant_ID int,complaint varchar(254),date_of_complaint date);")
    cursor.execute("create table Admin_Details(AID int primary key,Admin_name varchar(50),Email varchar(50),password varchar(50));")
    cursor.execute("insert into admin_details values(1,'Himangshu','kuchbhi@indiapost.com','12345678');")
    mydb.commit()
    print(Fore.GREEN+"SetUp Successful"+Style.RESET_ALL)
    
def get_pass():
    with open("password.dat","rb+") as f:
        try:
            password=pickle.load(f)
        except EOFError:
            from maskpass import advpass
            password=advpass("Enter your SQL password :")
            pickle.dump(password,f)
    return password


