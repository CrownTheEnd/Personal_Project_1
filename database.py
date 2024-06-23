import bcrypt
import math
import csv
import getpass

file = open("\\wsl.localhost\Ubuntu\home\crowntheend\Boot_dev\Personal_Project_1\database.csv", "r+")
file_info = file.read()
file.write("info")

data = {}
admin = {}
logged_in = False

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
    

def add_entry(website, password, username="", pin="", recovery_token=""):
    data[website] = password, username, pin, recovery_token


    
def delete_entry(data): # this still needs to be only accessible after the user has logged in
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
        
def get_user_input(): # this still needs to be only accessible after the user has logged in
    command = input("Enter 'next', 'prev', a page number, or 'return': ").strip().lower()
    return command

def items_per_page(data): # this still needs to be only accessible after the user has logged in
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
    
    
    
