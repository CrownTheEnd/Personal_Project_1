import bcrypt
import math
import csv
import getpass

#file = open("\\wsl.localhost\Ubuntu\home\crowntheend\Boot_dev\Personal_Project_1\database.csv", "r+")
#file_info = file.read()
#file.write("info")

data = {"pornhub.com": ("andass", "ilovedicks11", "80085", "G4MB4")}
admin = {"dicklover": "admin"}
logged_in = False

# Decorator definition
def requires_login(func):
    def wrapper(*args, **kwargs):
        if not logged_in:
            print("Error: Not logged in.")
            return
        return func(*args, **kwargs)
    return wrapper

def login(admin):
    global logged_in
    username = input("Please input username: ")
    if username in admin:
        password = getpass.getpass("Enter your password: ")
        if password == admin[username]:
            print("Succesfully logged in.")
            logged_in = True
        else:
            print("Wrong Password.")
    else:
        print("Username doesn't exist.")
        
def logout():
    global logged_in
    confirm = input("Are you sure you want to logout? y/n")
    if confirm.lower() == "y":
        print("Succesfully logged out.")
        logged_in = False
    elif confirm.lower() == "n":
            print("Understood, resuming operations.")
            return
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
    
@requires_login
def add_entry(website, password, username="", pin="", recovery_token=""):
    data[website] = password, username, pin, recovery_token

@requires_login
def delete_entry(data): 
    if len(data) == 0:
        print("Error: There are no saved passwords.")
        return
    
    while True:
        print("Please input a website to delete, type 'cancel' to exit or 'list' to list saved passwords:")
        selection = input("> ").strip().lower()
        
        if selection == 'cancel':
            print("Deletion canceled.")
            break
        
        elif selection == 'list':
            items_per_page(data)
            continue
        
        elif selection in data:
            confirmation = input(f"Are you sure you want to delete '{selection}'? (y/n): ").strip().lower()
            if confirmation == 'y':
                deleted_value = data.pop(selection)
                print(f"Deleted: {selection}: {deleted_value}")
                break
            elif confirmation == 'n':
                print("Deletion canceled.")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        
        else:
            print(f"Command '{selection}' not recognized or website '{selection}' not found in the data. Please try again.")

@requires_login
def modify_entry(data):
    if len(data) == 0:
        print("Error: There are no saved passwords.")
        return
    
    while True:
        print("Please input a website to modify, type 'cancel' to exit or 'list' to list saved passwords:")
        selection = input("> ").strip().lower()

        if selection == 'cancel':
            print("Modification canceled.")
            break
        
        elif selection == 'list':
            items_per_page(data)
            continue
        
        elif selection in data:
            confirmation = input(f"Which part of '{selection}' would you like to modify? (website/password/username/pin/rtoken): ").strip().lower()
            if confirmation == 'website':
                new_website = input("Please type in new website: ").strip()
                if new_website in data:
                    print("Error: The new website already exists in the data.")
                else:
                    value = data.pop(selection)
                    data[new_website] = value
                    print(f"Modified: {selection} to {new_website}")
                break
            elif confirmation == 'password':
                new_password = getpass.getpass("Please type in new password: ").strip()
                password, username, pin, recovery_token = data[selection]
                if new_password == password:
                    print("Error: This is already the password.")
                else:
                    data[selection] = (new_password, username, pin, recovery_token)
                    print("New password saved.")
                break
            elif confirmation == 'username':
                old_username = data[selection][1] #username is the 2nd index of data keys.
                new_username = input("Please type in new username: ").strip()
                password, username, pin, recovery_token = data[selection]
                if new_username == username:
                    print("Error: This is already the username.")
                else:
                    data[selection] = (password, new_username, pin, recovery_token)
                    print(f"Modified: {old_username} to {new_username}")
                break
            elif confirmation == 'pin':
                new_pin = getpass.getpass("Please type in new pin: ").strip()
                password, username, pin, recovery_token = data[selection]
                if new_pin == pin:
                    print("Error: This is already the pin.")
                else:
                    data[selection] = (password, username, new_pin, recovery_token)
                    print("New pin saved.")
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        
        else:
            print(f"Command '{selection}' not recognized or website '{selection}' not found in the data. Please try again.")
        
@requires_login        
def get_user_input(): 
    command = input("Enter 'next', 'prev', a page number, or 'return': ").strip().lower()
    return command

@requires_login
def items_per_page(data): 
    websites = sorted(list(data.items()))
    list_of_dicts = []
    item_range = 20
    current_page = 0
    pages = (len(websites) // 20) + (1 if len(websites) % 20 != 0 else 0)
    
    if len(websites) <= 20:
        print(f"Page 1: {websites}")
    else:
        while websites:
            pages_dict = {}
            for website, password in websites[:item_range]:
                pages_dict[website] = password
            list_of_dicts.append(pages_dict)
            websites = websites[item_range:]

    while True:
        print(f"Page {current_page + 1}: {list_of_dicts[current_page]}")
        command = get_user_input()

        if command == "next":
            if current_page < pages - 1:
                current_page += 1
            else:
                print("You are already on the last page.")
        elif command == "prev":
            if current_page > 0:
                current_page -= 1
            else:
                print("You are already on the first page.")
        elif command.isdigit():
            page_number = int(command) - 1
            if 0 <= page_number < pages:
                current_page = page_number
            else:
                print("Invalid page number.")
        elif command == "return":
            print("Returning to the previous command...")
            break
        else:
            print("Invalid command. Please enter 'next', 'prev', a page number, or 'return_to_previous'.")
    
    
    
