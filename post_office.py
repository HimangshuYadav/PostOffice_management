import mysql.connector as con
import csv
import mysql.connector.errors
from geopy.geocoders import Nominatim
from geopy.distance import distance
from math import ceil
from tabulate import tabulate
import os
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

def green_text(text:str):
    print(Fore.GREEN+text+Style.RESET_ALL)
def red_text(text:str):
    print(Fore.RED+text+Style.RESET_ALL)

def connect():
    mydb=con.connect(host="localhost",user="root",passwd="uhsgnamih")
    cursor=mydb.cursor()
    try:
        cursor.execute("use postoffice;")
        return cursor,mydb,True
    except mysql.connector.errors.ProgrammingError:
        red_text("Please run the setUp file First")
        return cursor,mydb,False
cursor,mydb,state=connect()

def Press_Enter():
    print("Press ENTER to Continue")
    input()
    clear_screen()

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
                    red_text("Invaild Input!!!\nPress ENTER to Continue")
                    input
                    clear_screen()
                    track_parcel(info,Update)
                updated_status.append(updated_status[0])
                # print(updated_status)
                try:
                    cursor.execute("update parcel_details set PID=%s,in_transit=%s,out_for_delivery=%s,delivered=%s,returned=%s,sender_add=%s,reciever_add=%s where PID=%s", updated_status)
                    mydb.commit()
                    green_text("Updated!!!")
                except mysql.connector.errors:
                    red_text("Something went wrong while updating")
                Press_Enter()
                parcel_management_menu()
            if opt.upper()=="N":
                clear_screen()
                parcel_management_menu()
             
    except TypeError:
        red_text("INVAILD Parcel ID \nTry Again!!!")
        Press_Enter()
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
    if weight_g <= 500:
        rate_per_km = 5  
    elif weight_g <= 2000:
        rate_per_km = 10  
    else:
        rate_per_km = 20  

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
        red_text("INVAILD INPUT TRY AGAIN")
        menu()
     
def Auth_Customer():
    title()
    print(figlet_format("Auth",font="mini"))
    new=input("you are New user???(y/n)")
    if new=="y":
        clear_screen()
        Register_Customer()
    elif new=="n":
        clear_screen()
        login_Customer()
    else:
        red_text("Invaild Input...")
        Press_Enter()
        Auth_Customer()

def login_Customer():
    title()
    print(figlet_format("Login",font="mini"))
    get_Lists("email",Email_List,"customer_details")
    email=input("Enter your email : ")
    if email not in Email_List:
        red_text("No User Found with email",email,)
        Press_Enter()
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
                red_text("Incorrect Password...")
                Press_Enter()
                login_Customer()
            else:
                red_text("3 Unsuccessful Attempts")
                Press_Enter()
                menu()
                #TODO 3 attempt thing is not working come here again
def Register_Customer():
    title()
    print(figlet_format("Register",font="mini"))
    get_Lists("email",Email_List,"customer_details")
    email=input("Enter Email :")
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
        try:
            cursor.execute("INSERT INTO customer_details (UID, email, password,name) VALUES (%s, %s, %s,%s)", (Userid, email, password,name))
            mydb.commit()
        except Exception:
            red_text("Something Went Wrong")
        clear_screen()
        login_Customer()
        

def Login_Staff():
    title()
    print(figlet_format("Login",font="mini"))
    get_Lists("email",SEmail_List,"staff_details")
    Email=input("Enter your Employee Email :")
    if Email not in SEmail_List:
        # print(SEmail_List)
        red_text("Incorrect Email...")
        Press_Enter()
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
                red_text("Incorrect Password...")
                Press_Enter()
                Login_Staff()
            else:
                red_text("3 Unsuccessful Attempts")
                Press_Enter()
                menu()
                #TODO attempts method
   
def Login_Admin():
    get_Lists("AID",AID_List,"admin_details")
    title()
    print(figlet_format("Login",font="mini"))
    AID=int(input("Enter Admin Id :"))
    if AID not in AID_List:
        # print(AID_List)
        red_text("Incorrect Admin ID...")
        Press_Enter()
        menu()
    else:
        cursor.execute(f"select password from admin_details where AID ='{AID}'")
        user_password=cursor.fetchone()[0]
        password=ask_pass()
        if user_password==password:
            clear_screen()
            Admin_Menu()
        else:
            red_text("Incorrect Password")
            Press_Enter()
            Login_Admin()
            
def Customer_Menu():
    title()
    print(figlet_format("Menu",font="mini"))
    print("[1]Track")
    print("[2]Locate post office") #Not sure how to make it work
    print("[3]Postage Calculator")
    print("[0]Logout")
    # print("")#TODO more features
    opt=int(input("Enter option :"))
    if opt==1:
        clear_screen()
        title()
        print(figlet_format("Track",font="mini"))
        PID=int(input("Enter parcel ID :"))
        cursor.execute(f"select * from parcel_details where PID={PID}")
        info=cursor.fetchone()
        track_parcel(info)
        Press_Enter()
        Customer_Menu()
    elif opt==2:
        clear_screen()
        title()
        print(figlet_format("Locate Post Office",font="mini"))
        district=input("Enter District:")
        nearest__po=nearest_po(district)
        if len(nearest__po)!=0:
            print(tabulate(nearest__po,["officename","pincode","Taluk","Districtname","statename"],tablefmt="fancy_grid"))
            Press_Enter()
            Customer_Menu()
        else:
            red_text("District not found!!!")
            Press_Enter()
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
        Press_Enter()
        Customer_Menu()
        
    elif opt==0:
        clear_screen()
        menu()
        
    else:
        red_text("INVAILD INPUT\ntry again...")
        Press_Enter()
        Customer_Menu()

def Staff_Menu():
    title()
    print(figlet_format("Menu",font="mini"))
    print("[1]Parcel Management")
    print("[2]Customer Services")
    print("[3]Complaint and Query Management")
    print("[0]Logout")
    opt=input("Enter option :")
    if opt=="1":
        clear_screen()
        parcel_management_menu()
    elif opt=="2":
        clear_screen()
        Customer_service_menu()
    elif opt=="3":
        clear_screen()
        Complaint_menu()
    elif opt=="0":
        clear_screen()
        menu()
    else:
        red_text("Invaild Input\nTry again")
        Press_Enter()
        Staff_Menu()

def parcel_management_menu():
    title()
    print(figlet_format("Parcel Management",font="mini"))
    print("[1]Register a New Parcel")
    print("[2]Update Parcel Status")
    print("[3]Track Parcel by ID")
    print("[4]View All Parcels by Status")
    print("[0]Exit")
    opt=input("Enter option :")
    if opt=="1":
        clear_screen()
        title()
        print(figlet_format("Register New Parcel",font="mini"))
        To=input("Enter Recievers Address :")
        From=input("Enter Senders Address :")
        cursor.execute("select PID from parcel_details order by PID desc;")
        last_PID=cursor.fetchone()[0]
        try:
            current_PID=last_PID+1
        except TypeError:
            current_PID=1
        print("Parcel ID :",green_text(f"{current_PID}"))
        while cursor.nextset():
            cursor.fetchall()
        try:
            cursor.execute("insert into parcel_details values(%s,false,false,false,false,%s,%s);",(current_PID,From,To))
            mydb.commit()
        except Exception:
            red_text("Something Went Wrong")
        Press_Enter()
        parcel_management_menu()
        
    elif opt=="2":
        get_Lists("PID",PID_List,"parcel_details")
        clear_screen()
        title()
        print(figlet_format("Update Parcel Status",font="mini"))
        PID=int(input("Enter parcel ID :"))
        if PID not in PID_List:
            red_text("INCORRECT ID!!!")
            Press_Enter()
            parcel_management_menu()
        else:
            cursor.execute(f"select * from parcel_details where PID ={PID}")
            info=cursor.fetchone()
            # print(info)
            track_parcel(info,True)
    elif opt=="3":
        clear_screen()
        title()
        print(figlet_format("Track Parcel",font="mini"))
        PID=int(input("Enter parcel ID :"))
        cursor.execute(f"select * from parcel_details where PID={PID}")
        info=cursor.fetchone()
        track_parcel(info)
        Press_Enter()
        parcel_management_menu()
    elif opt=="4":
        clear_screen()
        title()
        print(figlet_format("View All Parcels by Status",font="mini"))
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
                print(tabulate(out,["PID","Password","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
                Press_Enter()
                parcel_management_menu()
            else:
                red_text("No data found!!!")
                Press_Enter()
                parcel_management_menu()
                
        elif inp=="2":
            cursor.execute("select PID,sender_add,reciever_add from parcel_details where in_transit=true and out_for_delivery=true and delivered=false and returned=false")
            out=cursor.fetchall()
            if len(out)!=0:
                print(tabulate(out,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
                Press_Enter()
                parcel_management_menu()
            else:
                red_text("No data found!!!")
                Press_Enter()
                parcel_management_menu()
        if inp=="3":
            cursor.execute("select PID,sender_add,reciever_add from parcel_details where in_transit=true and out_for_delivery=true and delivered=true and returned=false")
            out=cursor.fetchall()
            if len(out)!=0:
                print(tabulate(out,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
                Press_Enter()
                parcel_management_menu()
            else:
                red_text("No data found!!!")
                Press_Enter()
                parcel_management_menu()
        if inp=="4":
            cursor.execute("select PID,sender_add,reciever_add from parcel_details where in_transit=true and out_for_delivery=true and delivered=true and returned=true")
            out=cursor.fetchall()
            if len(out)!=0:
                print(tabulate(out,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
                Press_Enter()
                parcel_management_menu()
            else:
                red_text("No data found!!!")
                Press_Enter()
                parcel_management_menu()
        if inp=='0':
            clear_screen()
            parcel_management_menu()
        else:
            red_text("Invaild Input")
            Press_Enter()
            parcel_management_menu()
    
    elif opt=="0":
        clear_screen()
        Staff_Menu()
        
    else:
        red_text("INVAILD INPUT")
        Press_Enter()
        parcel_management_menu()

def Customer_service_menu():
    title()
    print(figlet_format("Customer Management",font="mini"))
    print("[1]Register New Customer")
    print("[2]Search Customer by ID or Name")
    print("[0]Exit")
    opt=input("Enter option :")
    if opt=="1":
        clear_screen()
        Register_Customer()
    elif opt=="2":
        UID=input("Enter User ID or email:")
        cursor.execute("select * from customer_details where UID=%s or email=%s;",(UID,UID))
        info=cursor.fetchall()
        if len(info)!=0:
            print(tabulate(info,["PID","Sender Address","Reciever's Address"],tablefmt="fancy_grid"))
            Press_Enter()
            Customer_service_menu()
        else:
            red_text("No User found!!!")
            Press_Enter()
            Customer_service_menu()
            
    elif opt=="0":
        clear_screen()
        Staff_Menu()
            
    else:
        red_text("INVAILD INPUT")
        Press_Enter()
        Customer_service_menu()

def Complaint_menu():
    title()
    print(figlet_format("Complaint Management",font="mini"))
    print("[1]Register New Complaint")
    print("[2]View All Complaints")
    print("[3]Search Complaints by Customer ID")
    print("[0]Exit")
    opt=input("Enter option :")
    if opt=="1":
        clear_screen()
        title()
        print(figlet_format("New Complaint",font="mini"))
        CID=get_UID("complaint","CID")
        complainant=input("Enter complainant's name :")
        complainant_ID=input("Enter complainant's ID :")
        Complaint=next_line(input("Enter his Complaint :"))
        date = datetime.now().strftime('%Y-%m-%d')
        cursor.reset()
        try:
            cursor.execute("insert into complaint values(%s,%s,%s,%s,%s);",(CID,complainant,complainant_ID,Complaint,date))
            mydb.commit()
            green_text("Complaint Filed successfully!!!")
            Press_Enter()
            Complaint_menu()
        except Exception:
            red_text("Compalint too Long")
            Press_Enter()
            Complaint_menu()
        
    elif opt=="2":
        clear_screen()
        title()
        cursor.execute("select complainant_ID,complainant_name,complaint,date_of_complaint from complaint;")#TODO change issuer ro complainant
        data=cursor.fetchall()
        if len(data)!=0:
            print(tabulate(data,["Complainant ID","Complainant","Complaint","Date of complaint"],tablefmt="fancy_grid"))
        else:
            red_text("No complaint found!!!")
        Press_Enter()
        Complaint_menu()
    elif opt=="3":
        clear_screen()
        title()
        UID=input("Enter Customer ID :")
        cursor.execute(f"select complainant_ID,complainant_name,complaint,date_of_complaint from complaint where complainant_ID ={UID}; ")
        info=cursor.fetchall()
        if len(info)==0:
            red_text("No complaint Found!!!")
            Press_Enter()
            Complaint_menu()
        else:
            print(tabulate(info,["Complainant ID","Complainant","Complaint","Date of complaint"],tablefmt="fancy_grid"))
            Press_Enter()
            Complaint_menu()
            
    elif opt=="0":
        clear_screen()
        Staff_Menu()
    else:
        red_text("INVAILD INPUT\n Try Again")
        Press_Enter()
        Complaint_menu()
        

def Admin_Menu():
    title()
    print(figlet_format("Menu",font="mini"))
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
        red_text("INVAILD INPUT")
        Press_Enter()
        Admin_Menu()
 
def Register_Staff():
    title()
    get_Lists("email",SEmail_List,"staff_details")
    email=input("Enter Employye's Email")
    if email in SEmail_List:#TODO check this and adjust the code
        red_text("User already exist...Try Again")
        Press_Enter()
        Register_Staff()
    else:
        password=ask_pass()
        name=input("Enter the name of Employee :")
        SID=get_UID("staff_details","SID")
        cursor.fetchall()
        try:
            cursor.execute("insert into staff_details values(%s,%s,%s,%s);",(SID,password,name,email))
            mydb.commit()
            print("This is your Staff Id :",SID)
        except:
            red_text("Something Went Wrong")
        Press_Enter()
        Admin_Menu()
        
def Update_Staff():
    title()
    get_Lists("SID",SID_List,"staff_details")
    SId=int(input("Enter the Staff ID :"))
    if SId not in SID_List:
        red_text("No Staff found with SID",SId,"\nTry Again")
        Press_Enter()
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
                    green_text("Updation Successful")
                    Press_Enter()
                    Admin_Menu()
                    
                except Exception:
                    red_text("Updation Unsuccessful\nTry again")
                    Press_Enter()
                    Update_Staff()
            elif inp=="2":
                New_Name=input("Enter Updated name :")
                try:
                    cursor.execute("update staff_details set name=%s where SID=%s",(New_Name,SId))
                    mydb.commit()
                    green_text("Updation Successful")
                    Press_Enter()
                    Admin_Menu()
                    
                except Exception:
                    red_text("Updation Unsuccessful\nTry again")
                    Press_Enter()
                    Update_Staff()

        
def staff_management_menu():    
    title()
    print(figlet_format("Staff Management",font="mini"))
    print("[1]Register New Staff Member")
    print("[2]Update Staff Information")
    print("[3]View all Staff")
    print("[4]Remove Staff Members")
    print("[0]Exit")
    opt=input("Enter option :")
    if opt=="1":
        clear_screen()
        Register_Staff()
    elif opt=="2":
        clear_screen()
        Update_Staff()
    elif opt=="3":
        clear_screen()
        title()
        print(figlet_format("View All Staff",font="mini"))
        cursor.execute("Select * from staff_details;")
        details=cursor.fetchall()
        print(tabulate(details,["Staff ID","password","Name","Email"],tablefmt="fancy_grid"))
        Press_Enter()
        Admin_Menu()
    elif opt=="4":
        clear_screen()
        title()
        print(figlet_format("Remove Staff",font="mini"))
        SId=input("Enter SID of Staff to remove :")
        cursor.execute(f"select SID,name,email from staff_details where SID ={SId};")
        data=cursor.fetchone()
        print(tabulate([data],["User ID","Email","password"],tablefmt="fancy_grid"))
        inp=input("Are You sure to remove this staff?(y/n)")
        if inp.lower()=="y":
            get_Lists("AID",AID_List,"admin_details")
            AID=int(input("Enter Your Admin ID :"))
            if AID not in AID_List:
                red_text("Incorrect Admin ID")
                Press_Enter()
                Admin_Menu()
            else:
                cursor.execute(f"select password from admin_details where AID ={AID}")
                user_password=cursor.fetchone()[0]
                password=ask_pass()
                if user_password==password:
                    cursor.execute(f"DELETE FROM staff_details WHERE SID={SId};")
                    mydb.commit()
                    green_text("Staff deleted Successfully")
                    Press_Enter()
                    Admin_Menu()
                else:
                    red_text("Wrong password...")
                    Press_Enter()
                    staff_management_menu()
        elif inp.lower()=="n":
            Press_Enter()
            Admin_Menu()
        else:
            red_text("INVALID INPUT\nTry Again")
            Press_Enter()
            staff_management_menu()
            
    elif opt=="0":
        clear_screen()
        Admin_Menu()
 
def Customer_Management_menu():
    title()
    print(figlet_format("Customer Management",font="mini"))
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
            red_text("There is No Customer Registered")
        Press_Enter()
        Customer_Management_menu()
    elif opt=="2":
        UId=input("Enter User ID of User to remove :")
        cursor.execute(f"select UID,name,email from customer_details where UID={UId}")
        info=cursor.fetchone()
        print(tabulate([info],["UID","Name","Email"],tablefmt="fancy_grid"))
        inp=input("Are You sure to remove this User(y/n)")
        if inp.lower()=="y":
            AID=int(input("Enter Your Admin ID :"))
            if AID not in AID_List:
                red_text("Incorrect Admin ID")
                Press_Enter()
                Customer_Management_menu()
            else:
                cursor.execute(f"select password from customer_details where UID ={UId}")
                user_password=cursor.fetchone()[0]
                password=ask_pass()
                if user_password==password:
                    cursor.execute(f"DELETE FROM customer_details WHERE UID={UId};")
                    mydb.commit()
                    green_text("Customer deleted Successfully")
                    Press_Enter()
                    Admin_Menu()
                else:
                    red_text("Wrong password...")
                    Press_Enter()
                    Customer_Management_menu()
        elif inp.lower()=="n":
            Press_Enter()
            Customer_Management_menu()
        else:
            red_text("INVALID INPUT\nTry Again")
            Press_Enter()
            Customer_Management_menu()
    elif opt=="0":
        clear_screen()
        Admin_Menu()
    else:  
        red_text("INVAILD INPUT")
        Press_Enter()
        Customer_Management_menu()

if __name__=="__main__" and state==True:
    clear_screen()
    menu()
    
if __name__=="__main__" and state==False:
    red_text("Please run the setup File First")
   
    
