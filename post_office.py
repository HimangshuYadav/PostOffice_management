import mysql.connector as con
import csv
from geopy.geocoders import Nominatim
from geopy.distance import distance
from math import ceil
from tabulate import tabulate
import os
import time
from colorama import Fore,Style
from pyfiglet import figlet_format

UID_List=[]
SID_List=[]
AID_List=[]
PID_List=[]
Email_List=[]
attempts=0

mydb=con.connect(host="localhost",user="root",passwd="uhsgnamih")
cursor=mydb.cursor()
cursor.execute("use postoffice_test;")

def clear_screen():
    os.system('cls')

def get_Lists(string:str,to_List:list):
    if len(to_List)==0:
        cursor.execute(f"select {string} from customer")
        result=cursor.fetchall()
        for i in result:
            for info in i:
                to_List.append(info)
        
 
def get_UID():
    cursor.execute("select UID from customer order by UID desc;")
    return int(cursor.fetchone()[0])+1
    
def track_parcel():
    PID=input("Enter parcel ID :")
    cursor.execute(f"select * from parcel_details where PID={PID}")
    info=cursor.fetchone()
    try:
        if info[2]==0:
            #kuch nahi
            print("[IN TRANSIT]       [OUT FOR DELIVERY]       [DELIVERD]")
            
        elif info[2]==1 and info[3]==0 and info[4]==0 and info[5]==0 :
            #in transit
            print(Fore.GREEN+f"[IN TRANSIT]{Style.RESET_ALL}====   [OUT FOR DELIVERY]       [DELIVERD]")
            
        elif info[2]==1 and info[3]==1 and info[4]==0 and info[5]==0  :
            #out for delivery
            print(f"{Fore.GREEN}[IN TRANSIT]{Style.RESET_ALL}======={Fore.GREEN}[OUT FOR DELIVERY]{Style.RESET_ALL}==     [DELIVERD]")
            
        elif info[2]==1 and info[3]==1 and info[4]==1 and info[5]==0 :
            #delivered
            print(f"{Fore.GREEN}[IN TRANSIT]{Style.RESET_ALL}======={Fore.GREEN}[OUT FOR DELIVERY]{Style.RESET_ALL}======={Fore.GREEN}[DELIVERD]{Style.RESET_ALL}")
            
        elif info[2]==1 and info[3]==1 and info[4]==1 and info[5]==1 :
            #returned
            print(f"{Fore.GREEN}[IN TRANSIT]{Style.RESET_ALL}======={Fore.GREEN}[OUT FOR DELIVERY]{Style.RESET_ALL}========{Fore.GREEN}[DELIVERD]{Style.RESET_ALL}======={Fore.RED}[RETURNED]{Style.RESET_ALL}")
            
    except TypeError:
        print("INVAILD Parcel ID \nTry Again!!!")
        Customer_Menu()
        
     
def nearest_po(s:str):
    result_list=[]
    with open("post_office_data.csv","r") as f:
        obj=csv.reader(f)
        for row in obj:
            if row[3].upper()==s.upper():
                result_list.append(row)
    return result_list

def calculate_distance(location1, location2):
    geolocator=Nominatim(user_agent='distance_calculator')
    location1=geolocator.geocode(location1)
    location2=geolocator.geocode(location2)
    return distance((location1.latitude,location1.longitude),(location2.latitude,location2.longitude)).meters/1000

def calculate_parcel_cost(distance_km : float, weight_g : float):
    # Define rate per km based on weight slabs
    if weight_g <= 500:
        rate_per_km = 5  # example rate
    elif weight_g <= 2000:
        rate_per_km = 10  # example rate
    else:
        rate_per_km = 20  # example rate

    # Calculate cost
    cost = 10+rate_per_km * distance_km
    return ceil(cost/100)

def title():
    print(Fore.RED+figlet_format("INDIA POST",font="standard",justify="center"),Style.RESET_ALL)

'''
Tables to be made:
Customer details
UID(PK),name,email,password,history

staff details
SID(PK),name,

Admin details
AID(PK),name,password

parcel details
parcel_ID(PK),user,in_transit, out_for_delivery,delivered,returned

Inventory

Complaint
CID(PK),complaint,date of complaint

Finance

'''

def menu():
    title()
    print(figlet_format("Role",font="mini"))
    print("[1]Customer")
    print("[2]Staff")
    print("[3]Admin")
    print("[0]Exit")
    role=int(input("Enter role :"))
    if role==1:
        clear_screen()
        Auth_Customer()
    elif role==2:
        pass
    elif role==3:
        pass
    elif role==0:
        pass
    else:
        print("INVAILD INPUT TRY AGAIN")
        menu()
        
def Auth_Customer():
    new=input("you are New user???(y/n)")
    if new=="y":
        clear_screen()
        Register_Customer()
    elif new=="n":
        clear_screen()
        login_Customer()
    else:
        print("Invaild Input...try again")
        Auth_Customer()
    
def login_Customer():
    title()
    print(figlet_format("Login",font="mini"))
    get_Lists("email",Email_List)
    email=input("Enter your email : ")
    if email not in Email_List:
        print("No User Found with email",email,"\nTry Again!!!")
        time.sleep(2)
        clear_screen()
        login_Customer()
    else:
        cursor.execute(f"select password from customer where email ='{email}'")
        user_password=cursor.fetchone()[0]
        
        password=input("Enter password : ")
        if user_password==password:
            clear_screen()
            Customer_Menu()
        else:
            # attempts+=1
            if attempts<=3:
                print("Incorrect Password...try again")
                time.sleep(2)
                clear_screen()
                login_Customer()
            else:
                print("3 Unsuccessful Attempts")
                print("moving to main menu")
                time.sleep(3)
                clear_screen()
                menu()

    
def Register_Customer():
    title()
    print(figlet_format("Register",font="mini"))
    get_Lists("email",Email_List)
    email=input("Enter Your Email")
    if email in Email_List:
        print("User already exist...moving to login page..")
        login_Customer()
    else:
        password=input("Enter Password :")
        name=input("What should we call you??? :")
        Userid=get_UID()
        print("This is your UserId:",Userid)
        while cursor.nextset():
            cursor.fetchall()
        cursor.execute("INSERT INTO customer (UID, email, password) VALUES (%s, %s, %s)", (Userid, email, password))
        mydb.commit()
        
        #TODO in the org database name column should be inserted and a variable name is to be inserted in it

def Login_Staff():
    SID=input("Enter your staff ID :")
    if SID not in SID_List:
        print("Incorrect SID...try again")
        Login_Staff()
    else:
        password=input("Enter password :")
        #TODO password check
        
def Login_Admin():
    AID=input("Enter Admin Id")
    if AID not in AID_List:
        print("Incorrect Admin ID...\nmoving to Menu...")
        menu()
    else:
        password=input("Enter password")
        #TODO password check
        
def Customer_Menu():
    title()
    print(figlet_format("Menu",font="mini"))
    print("[1]Track")
    print("[2]Locate post office") #Not sure how to make it work
    print("[3]Postage Calculator")
    print("[0]Logout")
    print("")#TODO more features
    opt=int(input("Enter option :"))
    if opt==1:
        clear_screen()
        print(figlet_format("Track",font="mini"))
        track_parcel()
        print("PRESS Enter to continue!!!")
        next=input()
        clear_screen()
        Customer_Menu()
    elif opt==2:
        clear_screen()
        print(figlet_format("Locate Post Office",font="mini"))
        district=input("Enter District:")
        nearest__po=nearest_po(district)
        if len(nearest__po)!=0:
            print(tabulate(nearest__po,["officename","pincode","Taluk","Districtname","statename"],tablefmt="fancy_grid"))
            print("PRESS Enter to continue!!!")
            next=input()
            clear_screen()
            Customer_Menu()
        else:
            print("District not found!!!\nTry Again!!!")
            time.sleep(2)
            clear_screen()
            Customer_Menu()
            
        
    elif opt==3:
        clear_screen()
        print(figlet_format("Postage Calculator",font="mini"))
        mass=float(input("Enter weight of your parcel(in grams) : "))
        sender=input("Enter your address")
        receiver=input("Enter the reciever's address")
        distance=calculate_distance(sender,receiver)
        print(calculate_parcel_cost(distance,mass))
        print("PRESS Enter to continue!!!")
        next=input()
        clear_screen()
        Customer_Menu()
        
    elif opt==0:
        clear_screen()
        menu()
        
    else:
        print("INVAILD INPUT\ntry again...")
        time.sleep(2)
        Customer_Menu()
        

def Staff_Menu():
    print("[1]Parcel Management")
    print("[2]Customer Services")
    print("[3]Inventory Management")
    print("[4]Complaint and Query Management")
    print("[5]Daily Summaries")
    print("[6]Logout")
    opt=int(input("Enter option :"))
    if opt==1:
        parcel_management_menu()
    elif opt==2:
        Customer_service_menu()
    elif opt==3:
        Inventory_Management_menu()
    elif opt==4:
        Complaint_menu()
    elif opt==5:
        pass
    elif opt==6:
        #TODO change current user to ""
        pass
    
    
    
def parcel_management_menu():
    print("[1]Register a New Parcel")
    print("[2]Update Parcel Status")
    print("[3]Track Parcel by ID")
    print("[4]View All Parcels by Status")
    opt=int(input("Enter option :"))
    if opt==1:
        #TODO take all the details and last PID and add 1 to it get the new ID
        pass
    elif opt==2:
        PID=input("Enter parcel ID :")
        if PID not in PID_List:
            print("INCORRECT ID")
            #TODO try again (get this thing in a funtion)
        else:
            print("")
            #TODO menu to show status like in transit,delivered etc
    elif opt==3:
        PID=input("Enter parcel ID :")
        if PID not in PID_List:
            print("INCORRECT ID")
            #TODO try again (get this thing in a funtion)
        else:
            print("")
            #TODO show details
    elif opt==4:
        #TODO 
        pass
    
    
def Customer_service_menu():
    print("[1]Register New Customer")
    print("[2]Search Customer by ID or Name")
    print("[3]View Customer History")
    opt=int(input("Enter option :"))
    if opt==1:
        Register_Customer()
    elif opt==2:
        UID=input("Enter User ID :")
        #TODO search user 
    elif opt==3:
        #TODO something to show user history
        pass
    
    
def Inventory_Management_menu():
    print("[1]Check Inventory")
    print("[2]Update Inventory Levels")
    opt=int(input("Enter option :"))
    if opt==1:
        pass
    elif opt==2:
        pass
    
def Complaint_menu():
    print("[1]Register New Complaint")
    print("[2]Update Complaint Status")
    print("[3]View All Complaints")
    print("[4]Search Complaints by Customer ID")
    opt=int(input("Enter option :"))
    if opt==1:
        pass
    elif opt==2:
        pass
    elif opt==3:
        pass
    elif opt==4:
        pass
    
    

def Admin_Menu():
    print("[1]Staff management")
    print("[2]Customer Management")
    print("[3]Finance and Transactions")
    print("[4]Inventory and Supplies Management")
    print("[5]Reports and Analytics")
    print("[6]Logout")
    opt=int(input("Enter option :"))
    if opt==1:
        staff_management_menu()
    elif opt==2:
        Customer_Management_menu()
    elif opt==3:
        Finance_menu()
    elif opt==4:
        Inventory_menu()
    elif opt==5:
        pass
    elif opt==6:
        pass
 
def Register_Staff():
    email=input("Enter Employye's Email")
    if email in Email_List:#TODO check this and adjust the code
        print("User already exist...moving to login page..")
        login_Customer()
    else:
        password=input("Enter Password :")
        name=input("What should we call you??? :")
        print("This is your UserId")
        #TODO function to take last UId and add 1 to to create new UID
        
def Update_Staff():
    print("What you want to update")
    #TODO Check here after database is created
        
def staff_management_menu():    
    print("[1]Register New Staff Member")
    print("[2]Update Staff Information")
    print("[3]Assign Roles and Permissions")
    print("[4]Remove Staff Members")
    opt=int(input("Enter option :"))
    if opt==1:
        Register_Staff()
    elif opt==2:
        Update_Staff()
    elif opt==3:
        SID=input("Enter SID")
        #TODO check the existance and make a menu for this
    elif opt==4:
        SID=input("Enter SID")
        #TODO password check of admin and then delete staff
    
    
def Customer_Management_menu():
    print("[1]View and Manage Customer Records")
    print("[2]Delete Customer Data")
    print("[3]View Customer History")
    opt=int(input("Enter option :"))
    if opt==1:
        pass
    elif opt==2:
        pass
    elif opt==3:
        pass
    

def Finance_menu():
    print("[1]Access All Payment Records")
    print("[2]Generate Financial Reports")
    opt=int(input("Enter option :"))
    if opt==1:
        pass
    elif opt==2:
        pass

def Inventory_menu():
    print("[1]View Inventory Levels")
    print("[2]Update Inventory")
    print("[3]Track Supply Usage History")
    opt=int(input("Enter option :"))
    if opt==1:
        pass
    elif opt==2:
        pass
    elif opt==3:
        pass
    
if __name__=="__main__":
    clear_screen()
    menu()
