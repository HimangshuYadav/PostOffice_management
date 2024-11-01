import mysql.connector as con
import csv
from geopy.geocoders import Nominatim
from geopy.distance import distance
from math import ceil,floor
from tabulate import tabulate
import os
import time
from colorama import Fore,Style
from pyfiglet import figlet_format
from datetime import datetime

UID_List=[]
SID_List=[]
SEmail_List=[]
AID_List=[]
PID_List=[]
Email_List=[]
attempts=0

mydb=con.connect(host="localhost",user="root",passwd="uhsgnamih")
cursor=mydb.cursor()
cursor.execute("use postoffice_test;")

def clear_screen():
    os.system('cls')

def get_Lists(string:str,to_List:list,from_table:str):
    if len(to_List)==0:
        cursor.execute(f"select {string} from {from_table}")
        result=cursor.fetchall()
        for i in result:
            for info in i:
                to_List.append(info)
        
def next_line(text, line_length=50):
    return '\n'.join(text[i:i + line_length] for i in range(0, len(text), line_length))
 
def get_UID(table:str,ID:str):
    cursor.execute(f"select {ID} from {table} order by {ID} desc;")
    try:
        return int(cursor.fetchone()[0])+1
    except:
        return 1
    
def track_parcel(info:tuple,Update=False):
    try:
        if info[1]==0:
            #kuch nahi
            print("[IN TRANSIT]       [OUT FOR DELIVERY]       [DELIVERD]")
            
        if info[1]==1 and info[2]==0 and info[3]==0 and info[4]==0 :
            #in transit
            print(Fore.GREEN+f"[IN TRANSIT]{Style.RESET_ALL}====   [OUT FOR DELIVERY]       [DELIVERD]")
            
        if info[1]==1 and info[2]==1 and info[3]==0 and info[4]==0  :
            #out for delivery
            print(f"{Fore.GREEN}[IN TRANSIT]{Style.RESET_ALL}======={Fore.GREEN}[OUT FOR DELIVERY]{Style.RESET_ALL}==     [DELIVERD]")
            
        if info[1]==1 and info[2]==1 and info[3]==1 and info[4]==0 :
            #delivered
            print(f"{Fore.GREEN}[IN TRANSIT]{Style.RESET_ALL}======={Fore.GREEN}[OUT FOR DELIVERY]{Style.RESET_ALL}======={Fore.GREEN}[DELIVERD]{Style.RESET_ALL}")
            
        if info[1]==1 and info[2]==1 and info[3]==1 and info[4]==1 :
            #returned
            print(f"{Fore.GREEN}[IN TRANSIT]{Style.RESET_ALL}======={Fore.GREEN}[OUT FOR DELIVERY]{Style.RESET_ALL}========{Fore.GREEN}[DELIVERD]{Style.RESET_ALL}======={Fore.RED}[RETURNED]{Style.RESET_ALL}")
        if Update==True:
            
            updated_status=list(info)
            opt=input("Do you want to Update???(y/n) :")
            if opt.upper()=="Y":
                print("Current Status")
                print("[1]In Transit")  
                print("[2]Out For Delivery")  
                print("[3]Deliverd")  
                print("[4]Returned")
                status=input()
                if status=="1":
                    updated_status[1],updated_status[2],updated_status[3],updated_status[4]=[1,0,0,0]
                elif status=="2":
                    updated_status[1],updated_status[2],updated_status[3],updated_status[4]=[1,1,0,0]
                elif status=="3":
                    updated_status[1],updated_status[2],updated_status[3],updated_status[4]=[1,1,1,0]
                elif status=="4":
                   updated_status[1],updated_status[2],updated_status[3],updated_status[4]=[1,1,1,1]
                else:
                    print("Invaild Input!!!\n Try Again")
                    time.sleep(2)
                    clear_screen()
                    track_parcel(info,Update)
                updated_status.append(updated_status[0])
                print(updated_status)
                cursor.execute("update parcel_details set PID=%s,in_transit=%s,out_for_delivery=%s,delivered=%s,returned=%s,sender_add=%s,reciever_add=%s where PID=%s", updated_status)
                mydb.commit()
                print("Updated!!!\nPress Enter to Continue")
                inp=input()
                clear_screen()
                parcel_management_menu()
            if opt.upper()=="N":
                clear_screen()
                parcel_management_menu()
             
    except TypeError:
        print("INVAILD Parcel ID \nTry Again!!!")
        time.sleep(2)
        clear_screen()
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
        clear_screen()
        Login_Staff()
    elif role==3:
        clear_screen()
        Admin_Menu()
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
    get_Lists("email",Email_List,"customer")
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
                #TODO 3 attempt thing is not working come here again
def Register_Customer():
    title()
    print(figlet_format("Register",font="mini"))
    get_Lists("email",Email_List,"customer")
    email=input("Enter Your Email")
    if email in Email_List:
        print("User already exist...moving to login page..")
        login_Customer()
    else:
        password=input("Enter Password :")
        name=input("What should we call you??? :")
        Userid=get_UID("customer","UID")
        print("This is your UserId:",Userid)
        while cursor.nextset():
            cursor.fetchall()
        cursor.execute("INSERT INTO customer (UID, email, password) VALUES (%s, %s, %s)", (Userid, email, password))
        mydb.commit()
        
        #TODO in the org database name column should be inserted and a variable name is to be inserted in it

def Login_Staff():
    get_Lists("email",SEmail_List,"staff_details")
    Email=input("Enter your Employee Email :")
    if Email not in SEmail_List:
        print(SEmail_List)
        print("Incorrect Email...try again")
        time.sleep(2)
        clear_screen()
        Login_Staff()
    else:
        cursor.execute(f"select password from staff_details where email ='{Email}'")
        user_password=cursor.fetchone()[0]
        password=input("Enter password : ")
        if user_password==password:
            clear_screen()
            Staff_Menu()
        else:
            # attempts+=1
            if attempts<=3:
                print("Incorrect Password...try again")
                time.sleep(2)
                clear_screen()
                Login_Staff()
            else:
                print("3 Unsuccessful Attempts")
                print("moving to main menu")
                time.sleep(3)
                clear_screen()
                menu()
                #TODO attempts method
   
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
        PID=int(input("Enter parcel ID :"))
        cursor.execute(f"select * from parcel_details where PID={PID}")
        info=cursor.fetchone()
        track_parcel(info)
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
        clear_screen()
        Customer_Menu()

def Staff_Menu():
    print("[1]Parcel Management")
    print("[2]Customer Services")
    print("[3]Complaint and Query Management")
    print("[0]Logout")
    opt=int(input("Enter option :"))
    if opt==1:
        clear_screen()
        parcel_management_menu()
    elif opt==2:
        clear_screen()
        Customer_service_menu()
    elif opt==3:
        clear_screen()
        Complaint_menu()
    elif opt==0:
        clear_screen()
        menu()
    else:
        print("Invaild Input\nTry again")
        next=input()
        clear_screen()
        Staff_Menu()

def parcel_management_menu():
    print("[1]Register a New Parcel")
    print("[2]Update Parcel Status")
    print("[3]Track Parcel by ID")
    print("[4]View All Parcels by Status")
    opt=int(input("Enter option :"))
    if opt==1:
        To=input("Enter Recievers Address :")
        From=input("Enter Senders Address :")
        cursor.execute("select PID from parcel_details order by PID desc;")
        last_PID=cursor.fetchone()[0]
        current_PID=last_PID+1
        print("Parcel ID :",current_PID)
        while cursor.nextset():
            cursor.fetchall()
        cursor.execute("insert into parcel_details values(%s,false,false,false,false,%s,%s);",(current_PID,From,To))
        mydb.commit()
        print("Press Enter To Continue!!!")
        input()
        clear_screen()
        Staff_Menu()
        
    elif opt==2:
        get_Lists("PID",PID_List,"parcel_details")
        PID=int(input("Enter parcel ID :"))
        if PID not in PID_List:
            print("INCORRECT ID\nTry again!!!")
            time.sleep(2)
            clear_screen()
            parcel_management_menu()
        else:
            cursor.execute(f"select * from parcel_details where PID ={PID}")
            info=cursor.fetchone()
            print(info)
            track_parcel(info,True)
    elif opt==3:
        PID=int(input("Enter parcel ID :"))
        cursor.execute(f"select * from parcel_details where PID={PID}")
        info=cursor.fetchone()
        track_parcel(info)
        print("PRESS Enter to continue!!!")
        next=input()
        clear_screen()
        parcel_management_menu()
    elif opt==4:
        print("[1]In Transit")
        print("[2]Out for Delivery")
        print("[3]Deliverd")
        print("[3]Returned")
        inp=(input("Enter option :"))
        if inp=="1":
            cursor.execute("select PID,sender_add,reciever_add from parcel_details where in_transit=true and out_for_delivery=false and delivered=false and returned=false")
            out=cursor.fetchall()
            if len(out)!=0:
                print(tabulate(out,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
                print("PRESS Enter to continue!!!")
                next=input()
                clear_screen()
                parcel_management_menu()
            else:
                print("No data found!!!")
                next=input()
                clear_screen()
                parcel_management_menu()
                
        elif inp=="2":
            cursor.execute("select PID,sender_add,reciever_add from parcel_details where in_transit=true and out_for_delivery=true and delivered=false and returned=false")
            out=cursor.fetchall()
            if len(out)!=0:
                print(tabulate(out,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
                print("PRESS Enter to continue!!!")
                next=input()
                clear_screen()
                parcel_management_menu()
            else:
                print("No data found!!!")
                next=input()
                clear_screen()
                parcel_management_menu()
        if inp=="3":
            cursor.execute("select PID,sender_add,reciever_add from parcel_details where in_transit=true and out_for_delivery=true and delivered=true and returned=false")
            out=cursor.fetchall()
            if len(out)!=0:
                print(tabulate(out,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
                print("PRESS Enter to continue!!!")
                next=input()
                clear_screen()
                parcel_management_menu()
            else:
                print("No data found!!!")
                next=input()
                clear_screen()
                parcel_management_menu()
        if inp=="4":
            cursor.execute("select PID,sender_add,reciever_add from parcel_details where in_transit=true and out_for_delivery=true and delivered=true and returned=true")
            out=cursor.fetchall()
            if len(out)!=0:
                print(tabulate(out,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
                print("PRESS Enter to continue!!!")
                next=input()
                clear_screen()
                parcel_management_menu()
            else:
                print("No data found!!!")
                print("PRESS Enter to continue!!!")
                next=input()
                clear_screen()
                parcel_management_menu()

def Customer_service_menu():
    print("[1]Register New Customer")
    print("[2]Search Customer by ID or Name")
    opt=int(input("Enter option :"))
    if opt==1:
        Register_Customer()
    elif opt==2:
        UID=input("Enter User ID or email:")
        cursor.execute("select * from customer where UID=%s or email=%s;",(UID,UID))
        info=cursor.fetchall()
        if len(info)!=0:
            print(tabulate(info,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
            print("PRESS Enter to continue!!!")
            next=input()
            clear_screen()
            Customer_service_menu()
        else:
            print("No User found!!!")
            print("PRESS Enter to continue!!!")
            next=input()
            clear_screen()
            Customer_service_menu()
            
    else:
        print("INVAILD INPUT")
        print("PRESS Enter to continue!!!")
        next=input()
        clear_screen()
        Customer_service_menu()

def Complaint_menu():
    print("[1]Register New Complaint")
    print("[2]View All Complaints")
    print("[3]Search Complaints by Customer ID")
    opt=int(input("Enter option :"))
    if opt==1:
        CID=get_UID("complaint","CID")
        complainant=input("Enter complainant's name :")
        complainant_ID=input("Enter complainant's ID :")
        Complaint=next_line(input("Enter his Complaint :"))
        date = datetime.now().strftime('%Y-%m-%d')
        cursor.reset()
        try:
            cursor.execute("insert into complaint values(%s,%s,%s,%s,%s);",(CID,complainant,complainant_ID,Complaint,date))
            mydb.commit()
            print("Complaint Filed successfully!!!\nPress Enter to continue")
            next=input()
            clear_screen()
            Complaint_menu()
        except Exception:
            print("Compalint too Long")
            print("Press ENTER to continue!!")
            next=input()
            clear_screen()
            Complaint_menu()
        
    elif opt==2:
        cursor.execute("select complainant_ID,complainant_name,complaint,date_of_complaint from complaint;")#TODO change issuer ro complainant
        data=cursor.fetchall()
        if len(data)!=0:
            print(tabulate(data,["Complainant ID","Complainant","Complaint","Date of complaint"],tablefmt="fancy_grid"))
        else:
            print("No complaint found!!!")
        print("Press ENTER to continue")
        next=input()
        clear_screen()
        Complaint_menu()
    elif opt==3:
        pass
    else:
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
        clear_screen()
        staff_management_menu()
    elif opt==2:
        clear_screen()
        Customer_Management_menu()
    elif opt==3:
        clear_screen()
        Finance_menu()
    elif opt==4:
        clear_screen()
        Inventory_menu()
    elif opt==5:
        pass
    elif opt==6:
        pass
 
def Register_Staff():
    get_Lists("email",SEmail_List,"staff_details")
    email=input("Enter Employye's Email")
    if email in SEmail_List:#TODO check this and adjust the code
        print("User already exist...Try Again\nPress ENTER to Continue")
        input()
        clear_screen()
        Register_Staff()
    else:
        password=input("Enter Password :")
        name=input("Enter the name of Employee :")
        print("This is your UserId")
        SID=get_UID("staff_details","SID")
        cursor.execute("insert into staff_details values(%s,%s,%s,%s)",(SID,password,name,email))
        mydb.commit()
        print("Press ENTER to continue")
        input()
        clear_screen()
        Admin_Menu()
        
def Update_Staff():
    get_Lists("SID",SID_List,"staff_details")
    SId=int(input("Enter the Staff ID :"))
    if SId not in SID_List:
        print("No Staff found with SID",SId,"\nTry Again\nPress ENTER to Continue")
        input()
        clear_screen()
        Update_Staff()
        
    else:
        cursor.execute(f"select * from staff_details where SID={SId};")
        data=cursor.fetchone()
        print(data)
        print(tabulate([data],["Staff ID","password","Name","Email"],tablefmt="fancy_grid"))
        opt=input("Do you want to update this ???(y/n)")
        if opt.upper() =="Y":
            print("[1]Email")
            print("[2]Name")
            #TODO Add more details in staff details
            inp=input("Enter your option :")
            if inp=="1":
                New_Email=input("Enter new email :")
                try:
                    cursor.execute("update staff_details set email=%s where SID=%s",(New_Email,SId))
                    mydb.commit()
                    print("Updation Successful\nPress ENTER to Continue")
                    input()
                    clear_screen()
                    Admin_Menu()
                    
                except Exception as e:
                    print("Updation Unsuccessful\nTry again\Press ENTER to Continue")
                    print(e)
                    input()
                    clear_screen()
                    Update_Staff()

        
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