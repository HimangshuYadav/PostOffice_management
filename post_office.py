import mysql.connector as con
import csv
from geopy.geocoders import Nominatim
from geopy.distance import distance
from math import ceil
from tabulate import tabulate
import os
import time
from maskpass import advpass
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
cursor.execute("use postoffice;")

def clear_screen():
    os.system('cls')
    
def ask_pass():
    password=advpass()
    if len(password)<8:
        print("Lenght of password should be more than 8\nPress ENTER Try again")
        input()
        ask_pass()
    else:
        return password
        

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
                # print(updated_status)
                cursor.execute("update parcel_details set PID=%s,in_transit=%s,out_for_delivery=%s,delivered=%s,returned=%s,sender_add=%s,reciever_add=%s where PID=%s", updated_status)
                mydb.commit()
                print("Updated!!!\nPress Enter to Continue")
                input()
                clear_screen()
                parcel_management_menu()
            if opt.upper()=="N":
                clear_screen()
                parcel_management_menu()
             
    except TypeError:
        print("INVAILD Parcel ID \nTry Again!!!\nPress ENTER to Continue")
        input()
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
    try:
        geolocator=Nominatim(user_agent='distance_calculator')
        location1=geolocator.geocode(location1)
        location2=geolocator.geocode(location2)
        return distance((location1.latitude,location1.longitude),(location2.latitude,location2.longitude)).meters/1000
    except:
        return 1000
   


def calculate_parcel_cost(distance_km : float, weight_g : float):
    # Define rate per km based on weight slabs
    if weight_g <= 500:
        rate_per_km = 5  # example rate
    elif weight_g <= 2000:
        rate_per_km = 10  # example rate
    else:
        rate_per_km = 20  # example rate

    # Calculate cost
    try:
        cost = 10+rate_per_km * distance_km
        return ceil(cost/100)
    except TypeError:
        return 100

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
        Login_Admin()
    elif role==0:
        pass
    else:
        print("INVAILD INPUT TRY AGAIN")
        menu()
     
def Auth_Customer():
    title()
    new=input("you are New user???(y/n)")
    if new=="y":
        clear_screen()
        Register_Customer()
    elif new=="n":
        clear_screen()
        login_Customer()
    else:
        print("Invaild Input...Press ENTER to Continue")
        input()
        clear_screen()
        Auth_Customer()

def login_Customer():
    title()
    print(figlet_format("Login",font="mini"))
    get_Lists("email",Email_List,"customer_details")
    email=input("Enter your email : ")
    if email not in Email_List:
        print("No User Found with email",email,"\nTry Again!!!")
        time.sleep(2)
        clear_screen()
        login_Customer()
    else:
        cursor.execute(f"select password from customer_details where email ='{email}'")
        user_password=cursor.fetchone()[0]
        
        password=ask_pass()
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
    get_Lists("email",Email_List,"customer_details")
    email=input("Enter Your Email")
    if email in Email_List:
        print("User already exist...moving to login page..")
        login_Customer()
    else:
        password=ask_pass()
        name=input("What should we call you??? :")
        Userid=get_UID("customer_details","UID")
        print("This is your UserId:",Userid)
        while cursor.nextset():
            cursor.fetchall()
        cursor.execute("INSERT INTO customer_details (UID, email, password,name) VALUES (%s, %s, %s,%s)", (Userid, email, password,name))
        mydb.commit()
        clear_screen()
        login_Customer()
        

def Login_Staff():
    title()
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
        password=ask_pass()
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
    get_Lists("AID",AID_List,"admin_details")
    title()
    AID=int(input("Enter Admin Id :"))
    if AID not in AID_List:
        print(AID_List)
        print("Incorrect Admin ID...\nPress ENTER Continue")
        input()
        clear_screen()
        menu()
    else:
        cursor.execute(f"select password from admin_details where AID ='{AID}'")
        user_password=cursor.fetchone()[0]
        password=ask_pass()
        if user_password==password:
            clear_screen()
            Admin_Menu()
        else:
            print("Incorrect Pasword")
            
        
        
  
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
        title()
        print(figlet_format("Track",font="mini"))
        PID=int(input("Enter parcel ID :"))
        cursor.execute(f"select * from parcel_details where PID={PID}")
        info=cursor.fetchone()
        track_parcel(info)
        print("PRESS Enter to continue!!!")
        input()
        clear_screen()
        Customer_Menu()
    elif opt==2:
        clear_screen()
        title()
        print(figlet_format("Locate Post Office",font="mini"))
        district=input("Enter District:")
        nearest__po=nearest_po(district)
        if len(nearest__po)!=0:
            print(tabulate(nearest__po,["officename","pincode","Taluk","Districtname","statename"],tablefmt="fancy_grid"))
            print("PRESS Enter to continue!!!")
            input()
            clear_screen()
            Customer_Menu()
        else:
            print("District not found!!!\nPress ENTER to Continue")
            input()
            clear_screen()
            Customer_Menu()
            
        
    elif opt==3:
        clear_screen()
        title()
        print(figlet_format("Postage Calculator",font="mini"))
        mass=float(input("Enter weight of your parcel(in grams) : "))
        sender=input("Enter your address")
        receiver=input("Enter the reciever's address")
        distance=calculate_distance(sender,receiver)
        print(calculate_parcel_cost(distance,mass))
        print("PRESS Enter to continue!!!")
        input()
        clear_screen()
        Customer_Menu()
        
    elif opt==0:
        clear_screen()
        menu()
        
    else:
        print("INVAILD INPUT\ntry again...\nPress ENTER to Continue")
        input()
        clear_screen()
        Customer_Menu()

def Staff_Menu():
    title()
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
        input()
        clear_screen()
        Staff_Menu()

def parcel_management_menu():
    title()
    print("[1]Register a New Parcel")
    print("[2]Update Parcel Status")
    print("[3]Track Parcel by ID")
    print("[4]View All Parcels by Status")
    print("[0]Exit")
    opt=input("Enter option :")
    if opt=="1":
        clear_screen()
        title()
        To=input("Enter Recievers Address :")
        From=input("Enter Senders Address :")
        cursor.execute("select PID from parcel_details order by PID desc;")
        last_PID=cursor.fetchone()[0]
        try:
            current_PID=last_PID+1
        except TypeError:
            current_PID=1
        print("Parcel ID :",current_PID)
        while cursor.nextset():
            cursor.fetchall()
        cursor.execute("insert into parcel_details values(%s,false,false,false,false,%s,%s);",(current_PID,From,To))
        mydb.commit()
        print("Press Enter To Continue!!!")
        input()
        clear_screen()
        parcel_management_menu()
        
    elif opt=="2":
        clear_screen()
        title()
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
            # print(info)
            track_parcel(info,True)
    elif opt=="3":
        clear_screen()
        title()
        PID=int(input("Enter parcel ID :"))
        cursor.execute(f"select * from parcel_details where PID={PID}")
        info=cursor.fetchone()
        track_parcel(info)
        print("PRESS Enter to continue!!!")
        input()
        clear_screen()
        parcel_management_menu()
    elif opt=="4":
        clear_screen()
        title()
        print("[1]In Transit")
        print("[2]Out for Delivery")
        print("[3]Deliverd")
        print("[4]Returned")
        print("[0]Exit")
        inp=(input("Enter option :"))
        if inp=="1":
            cursor.execute("select PID,sender_add,reciever_add from parcel_details where in_transit=true and out_for_delivery=false and delivered=false and returned=false")
            out=cursor.fetchall()
            if len(out)!=0:
                print(tabulate(out,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
                print("PRESS Enter to continue!!!")
                input()
                clear_screen()
                parcel_management_menu()
            else:
                print("No data found!!!")
                input()
                clear_screen()
                parcel_management_menu()
                
        elif inp=="2":
            cursor.execute("select PID,sender_add,reciever_add from parcel_details where in_transit=true and out_for_delivery=true and delivered=false and returned=false")
            out=cursor.fetchall()
            if len(out)!=0:
                print(tabulate(out,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
                print("PRESS Enter to continue!!!")
                input()
                clear_screen()
                parcel_management_menu()
            else:
                print("No data found!!!")
                input()
                clear_screen()
                parcel_management_menu()
        if inp=="3":
            cursor.execute("select PID,sender_add,reciever_add from parcel_details where in_transit=true and out_for_delivery=true and delivered=true and returned=false")
            out=cursor.fetchall()
            if len(out)!=0:
                print(tabulate(out,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
                print("PRESS Enter to continue!!!")
                input()
                clear_screen()
                parcel_management_menu()
            else:
                print("No data found!!!")
                input()
                clear_screen()
                parcel_management_menu()
        if inp=="4":
            cursor.execute("select PID,sender_add,reciever_add from parcel_details where in_transit=true and out_for_delivery=true and delivered=true and returned=true")
            out=cursor.fetchall()
            if len(out)!=0:
                print(tabulate(out,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
                print("PRESS Enter to continue!!!")
                input()
                clear_screen()
                parcel_management_menu()
            else:
                print("No data found!!!")
                print("PRESS Enter to continue!!!")
                input()
                clear_screen()
                parcel_management_menu()
        if inp=='0':
            clear_screen()
            parcel_management_menu()
        else:
            print("Invaild Input\nPress ENTER to Continue")
            input()
            clear_screen()
            parcel_management_menu()
    
    elif opt=="0":
        clear_screen()
        Staff_Menu()
        
    else:
        print("INVAILD INPUT\nPress ENTER to Continue")
        input()
        clear_screen()
        parcel_management_menu()

def Customer_service_menu():
    title()
    print("[1]Register New Customer")
    print("[2]Search Customer by ID or Name")
    print("[0]Exit")
    opt=int(input("Enter option :"))
    if opt==1:
        Register_Customer()
    elif opt==2:
        UID=input("Enter User ID or email:")
        cursor.execute("select * from customer_details where UID=%s or email=%s;",(UID,UID))
        info=cursor.fetchall()
        if len(info)!=0:
            print(tabulate(info,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
            print("PRESS Enter to continue!!!")
            input()
            clear_screen()
            Customer_service_menu()
        else:
            print("No User found!!!")
            print("PRESS Enter to continue!!!")
            input()
            clear_screen()
            Customer_service_menu()
            
    elif opt=="0":
        clear_screen()
        Staff_Menu()
            
    else:
        print("INVAILD INPUT\nPRESS Enter to continue!!!")
        input()
        clear_screen()
        Customer_service_menu()

def Complaint_menu():
    title()
    print("[1]Register New Complaint")
    print("[2]View All Complaints")
    print("[3]Search Complaints by Customer ID")
    print("[0]Exit")
    opt=input("Enter option :")
    if opt=="1":
        clear_screen()
        title()
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
            input()
            clear_screen()
            Complaint_menu()
        except Exception:
            print("Compalint too Long")
            print("Press ENTER to continue!!")
            input()
            clear_screen()
            Complaint_menu()
        
    elif opt=="2":
        clear_screen()
        title()
        cursor.execute("select complainant_ID,complainant_name,complaint,date_of_complaint from complaint;")#TODO change issuer ro complainant
        data=cursor.fetchall()
        if len(data)!=0:
            print(tabulate(data,["Complainant ID","Complainant","Complaint","Date of complaint"],tablefmt="fancy_grid"))
        else:
            print("No complaint found!!!")
        print("Press ENTER to continue")
        input()
        clear_screen()
        Complaint_menu()
    elif opt=="3":
        clear_screen()
        title()
        UID=input("Enter Customer ID :")
        cursor.execute(f"select complainant_ID,complainant_name,complaint,date_of_complaint from complaint where complainant_ID ={UID}; ")
        info=cursor.fetchall()
        if len(info)==0:
            print("No complaint Found!!!\nPress ENTER to Continue")
            input()
            clear_screen()
            Complaint_menu()
        else:
            print(tabulate(info,["Complainant ID","Complainant","Complaint","Date of complaint"],tablefmt="fancy_grid"))
            print("Press ENTER to Continue")
            input()
            clear_screen()
            Complaint_menu()
            
    elif opt=="0":
        clear_screen()
        Staff_Menu()
    else:
        print("INVAILD INPUT\n Try Again\Press ENTER to Continue")
        input()
        clear_screen()
        Complaint_menu()
        

def Admin_Menu():
    title()
    print("[1]Staff management")
    print("[2]Customer Management")
    print("[0]Logout")
    opt=input("Enter option :")
    if opt=="1":
        clear_screen()
        staff_management_menu()
    elif opt=="2":
        clear_screen()
        Customer_Management_menu()
    elif opt=="0":
        clear_screen()
        menu()
    else:
        print("INVAILD INPUT\nPress ENTER to Continue")
        input()
        clear_screen()
        Admin_Menu()
 
def Register_Staff():
    get_Lists("email",SEmail_List,"staff_details")
    email=input("Enter Employye's Email")
    if email in SEmail_List:#TODO check this and adjust the code
        print("User already exist...Try Again\nPress ENTER to Continue")
        input()
        clear_screen()
        Register_Staff()
    else:
        password=ask_pass()
        name=input("Enter the name of Employee :")
        SID=get_UID("staff_details","SID")
        cursor.fetchall()
        cursor.execute("insert into staff_details values(%s,%s,%s,%s);",(SID,password,name,email))
        mydb.commit()
        print("This is your UserId",SID)
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
        # print(data)
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
                    
                except Exception:
                    print("Updation Unsuccessful\nTry again\Press ENTER to Continue")
                    input()
                    clear_screen()
                    Update_Staff()
            elif inp=="2":
                New_Name=input("Enter Updated name :")
                try:
                    cursor.execute("update staff_details set name=%s where SID=%s",(New_Name,SId))
                    mydb.commit()
                    print("Updation Successful\nPress ENTER to Continue")
                    input()
                    clear_screen()
                    Admin_Menu()
                    
                except Exception:
                    print("Updation Unsuccessful\nTry again\Press ENTER to Continue")
                    input()
                    clear_screen()
                    Update_Staff()

        
def staff_management_menu():    
    print("[1]Register New Staff Member")
    print("[2]Update Staff Information")
    print("[3]View all Staff")
    print("[4]Remove Staff Members")
    print("[0]Exit")
    opt=input("Enter option :")
    if opt=="1":
        Register_Staff()
    elif opt=="2":
        Update_Staff()
    elif opt=="3":
        cursor.execute("Select * from staff_details;")
        details=cursor.fetchall()
        print(tabulate(details,["Staff ID","password","Name","Email"],tablefmt="fancy_grid"))
        print("Press ENTER to Continue")
        input()
        clear_screen()
        Admin_Menu()
    elif opt=="4":
        SId=input("Enter SID of Staff to remove :")
        cursor.execute(f"select SID,name,email from staff_details where SID ={SId};")
        data=cursor.fetchone()
        print(tabulate([data],["User ID","Email","password"],tablefmt="fancy_grid"))
        inp=input("Are You sure to remove this staff(y/n)")
        if inp.lower()=="y":
            get_Lists("AID",AID_List,"admin_details")
            AID=int(input("Enter Your Admin ID :"))
            if AID not in AID_List:
                print("Incorrect Admin ID\nPress Enter To navigate to Admin Menu")
                input()
                clear_screen()
                Admin_Menu()
            else:
                cursor.execute(f"select password from admin_details where AID ={AID}")
                user_password=cursor.fetchone()[0]
                password=ask_pass()
                if user_password==password:
                    cursor.execute(f"DELETE FROM staff_details WHERE SID={SId};")
                    mydb.commit()
                    print("Staff deleted Successfully\nPress ENTER to continue")
                    input()
                    clear_screen()
                    Admin_Menu()
                else:
                    print("Wrong password...\nPress ENTER to continue")
                    input()
                    clear_screen()
                    staff_management_menu()
        elif inp.lower()=="n":
            print("Press ENTER to Continue")
            input()
            clear_screen()
            Admin_Menu()
        else:
            print("INVALID INPUT\nTry Again")
            print("Press ENTER to continue")
            input()
            clear_screen()
            staff_management_menu()
            
    elif opt=="0":
        clear_screen()
        Admin_Menu()
 
def Customer_Management_menu():
    print("[1]View Customer Records")
    print("[2]Delete Customer Data")
    print("[0]Exit")
    opt=input("Enter option :")
    if opt=="1":
        cursor.execute("select * from customer_details ;")
        data=cursor.fetchall()
        if len(data)!=0:
            print(tabulate(data,["User ID","password","name","email"],tablefmt="fancy_grid"))
        else:
            print("There is No Customer Registered")
        print("Press ENTER to continue")
        input()
        clear_screen()
        Customer_Management_menu()
    elif opt=="2":
        UId=input("Enter User ID of User to remove :")
        inp=input("Are You sure to remove this staff:")
        if inp.lower()=="y":
            AID=input("Enter Your Admin ID :")
            if AID not in AID_List:
                print("Incorrect Admin ID\nPress Enter To navigate to Admin Menu")
                input()
                clear_screen()
                Customer_Management_menu()
            else:
                cursor.execute(f"select password from customer_details where UID ='{UId}'")
                user_password=cursor.fetchone()[0]
                password=ask_pass()
                if user_password==password:
                    cursor.execute("DELETE FROM customer_details WHERE UID=%s;",(UId))
                    mydb.commit()
                    print("Customer deleted Successfully\nPress ENTER to continue")
                    input()
                    clear_screen()
                    Admin_Menu()
                else:
                    print("Wrong password...\nPress ENTER to continue")
                    input()
                    clear_screen()
                    Customer_Management_menu()
        elif inp.lower()=="n":
            print("Press ENTER to Continue")
            input()
            clear_screen()
            Customer_Management_menu()
        else:
            print("INVALID INPUT\nTry Again")
            print("Press ENTER to continue")
            input()
            clear_screen()
            Customer_Management_menu()
    elif opt=="0":
        clear_screen()
        Admin_Menu()
    else:  
        print("INVAILD INPUT\nPress ENTER to continue")
        input()
        clear_screen()
        Customer_Management_menu()

if __name__=="__main__":
    clear_screen()
    menu()