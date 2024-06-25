import getpass
import database
import ast
from utility_functions import write_to_database, write_to_users
from database import (data, admin, requires_login)

with open('/home/crowntheend/Boot_dev/Personal_Project_1/database.txt', 'r') as file:
    data_content = file.read()
if data_content != "": 
    data = ast.literal_eval(data_content) 
else: 
    data = {}
    
with open('/home/crowntheend/Boot_dev/Personal_Project_1/users.txt', 'r') as file:
    admin_content = file.read()
if admin_content != "": 
    admin = ast.literal_eval(admin_content) 
else: 
    admin = {}

def main():
    global admin
    if len(admin) < 1:
        confirmation = input("No user records found, would you like to create a user? y/n:\n")
        if confirmation.lower() == "y":
            
            username = input("Please type in a username:\n")
            password = getpass.getpass("Please type in a password:\n")
            admin[username] = password
            write_to_users(admin)
            print("Account successfully created, you may now login!\n")
        
        elif confirmation.lower() == "n":
            return
        
        else:
            print("Incorrect input! Exiting...")
            return
        
    database.login(admin)
    while database.logged_in == True:
        print("Please choose an option from the following: ")
        print("1: Add entry.")
        print("2: Modify entry.")
        print("3: Delete entry.")
        print("4: List entries.")
        print("5: Logout")
        option_number = input()
        if option_number == "1":
            website_input = input("Please input the website name: ")
            if website_input in data:
                print("Error: This website already has an entry!")
            elif len(website_input) < 1:
                print("Error: Field was left empty!")
            else:
                password_input = getpass.getpass("Please input the password: ")
                if len(password_input) < 1:
                    print("Error: Field was left empty!")
                else:    
                    username_input = input("Please input the username or hit 'enter' to skip: ")
                    pin_input = getpass.getpass("Please input the pin or hit 'enter' to skip: ")
                    rtoken_input = input("Please input the recovery token or hit 'enter' to skip: ")
                    data[website_input] = password_input, username_input, pin_input, rtoken_input
                    write_to_database(data)
        if option_number == "2":
            database.modify_entry(data)
            write_to_database(data)
        if option_number == "3":
            database.delete_entry(data)
            write_to_database(data)
        if option_number == "4":
            database.items_per_page(data)
        if option_number == "5":
            database.logout()


                
    #database.logout()
    
    
if __name__ == "__main__":
    main()