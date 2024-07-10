import getpass
import database
import ast
import os
from utility_functions import write_to_database, write_to_users, generate_token, read_zip, hash_password, check_password 
from database import (data, admin, current_user, logged_in)
    
file_path = './users.txt'
if not os.path.exists(file_path):
  file = open(file_path, "w")
  file.close()

with open(file_path, 'r') as file:
    admin_content = file.read()
if admin_content != "": 
    admin = ast.literal_eval(admin_content) 
else: 
    admin = {}
    
os.makedirs("./database", exist_ok=True)

def main():
    global admin
    global data
    global current_user
    if len(admin) < 1:
        confirmation = input("No user records found, would you like to create a user? y/n:\n")
        if confirmation.lower() == "y":
            
            username = input("Please type in a username:\n")
            password = getpass.getpass("Please type in a password:\n")
            hashed_password = hash_password(password)
            token = generate_token(20)
            hashed_token = hash_password(token)
            file_name = f"./database/{generate_token(20)}.zip"
            admin[username] = [hashed_password, hashed_token, file_name]
            write_to_users(admin)
            
            final = input(f"Your recovery key is: '{token}'\nPlease keep it safe in case you ever wish to recover the account. Type 'ok' to continue.\n")
            type_ok = ""
            if final != "ok":
                while type_ok.lower() != "ok":
                    type_ok = input("Type 'ok' to continue.\n")
                    if type_ok.lower() != "ok":
                        print("Incorrect input!")
            print("Account successfully created, you may now login!\n")
                
        elif confirmation.lower() == "n":
            return
        
        else:
            print("Incorrect input! Exiting...")
            return
        
    database.login(admin)
    data_content = read_zip(current_user[1], current_user[2])

    if data_content != "": 
        data = ast.literal_eval(data_content) 
    else: 
        data = {}
    
    while database.logged_in == True:
        print("Please choose an option from the following: ")
        print("1: Add entry.")
        print("2: Modify entry.")
        print("3: Delete entry.")
        print("4: List entries.")
        print("5: Logout\n")
        print("6: PURGE DATABASE")
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
                    data[website_input] = [password_input, username_input, pin_input, rtoken_input]
                    write_to_database(data, current_user[1], current_user[2])
        if option_number == "2":
            print(f"{current_user}")
            database.modify_entry(data, admin)
            write_to_database(data, current_user[1], current_user[2])
        if option_number == "3":
            database.delete_entry(data)
            write_to_database(data, current_user[1], current_user[2])
        if option_number == "4":
            while len(data) < 1:
                print("Error: No entries, please create some.\n")
                break
            else:
                database.items_per_page(data)
        if option_number == "5":
            database.logout()
        if option_number == "6":
            confirmation = input("Are you sure you want to delete all users and their associated information? y/n:\n")
            
            # Check if initial confirmation is valid
            while len(confirmation) > 1 or confirmation.lower() not in ("y", "n"):
                confirmation = input("Invalid input! Please type y/n or hit 'enter' to exit.\n")
                if confirmation.lower() == "n" or len(confirmation) < 1:
                    print("Cancelling operation...")
                    return
            
            if confirmation.lower() == "y":
                final = input("Final confirmation, do you really want to delete everything? y/n:\n")
                
                # Check if final confirmation is valid
                while len(final) > 1 or final.lower() not in ("y", "n"):
                    final = input("Invalid input! Please type y/n or hit 'enter' to exit.\n")
                    if final.lower() == "n" or len(final) < 1:
                        print("Cancelling operation...")
                        break
                if final.lower() == "y":
                    print("Deleting database...")
                    data = {}
                    write_to_database(data, current_user[1], current_user[2])
                    admin = {}
                    write_to_users(admin)
                    print("Logging out for the last time.")
                    print("Successfully logged out.")
                    database.logged_in = False
                    current_user = ""
                elif final.lower() == "n":
                    print("Cancelling operation...")
            elif confirmation.lower() == "n":
                print("Cancelling operation...")
                return

if __name__ == "__main__":
    main()