import getpass
from utility_functions import check_password, hash_password, write_to_users

data = {}
admin = {}
logged_in = False
current_user = []

# Decorator definition
def requires_login(func):
    def wrapper(*args, **kwargs):
        if not logged_in:
            print("Error: Not logged in.")
            return
        return func(*args, **kwargs)
    return wrapper

def login(admin): # add return to exit! don't forget
    global logged_in
    global current_user
    username = input("Please input username: ")
    if username in admin:
        password = getpass.getpass("Enter your password or if you have forgotten your password, type help: ")
        if check_password(password, admin[username][0]):
            print("Succesfully logged in.")
            logged_in = True
            current_user.append(username)
            current_user.append(password)
            current_user.append(admin[username][2])
        elif password == "help":
            recover = input("Please type in your recovery token.\n")
            if check_password(recover, admin[username][1]):
                new_password = getpass.getpass("Please type in your new password: ")
                hashed_new_password = hash_password(new_password)
                admin[username][0] = hashed_new_password
                print(f"Password successfully reset!")
                write_to_users(admin)
                login(admin)
            else:
                print("Wrong token.\n")    
        else:
            print("Wrong Password.")
    elif len(username) > 1 and username not in admin:
        print("Username doesn't exist.")
        login(admin)
    else:
        if len(username) < 1:
            return
        
def logout():
    global logged_in
    global current_user
    confirm = input("Are you sure you want to logout? y/n\n")
    if confirm.lower() == "y":
        print("Succesfully logged out.")
        logged_in = False
        current_user = []
        return
    elif confirm.lower() == "n":
            print("Understood, resuming operations.")
            return
    else:
        print("Invalid input. Please enter 'y' or 'n'.\n")
    



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
                data.pop(selection)
                print(f"Deleted information for: {selection}")
                break
            elif confirmation == 'n':
                print("Deletion canceled.")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        
        else:
            print(f"Command '{selection}' not recognized or website '{selection}' not found in the data. Please try again.")

@requires_login
def modify_entry(data, admin):
    if len(data) == 0 and len(admin) == 0:
        print("Error: There are no saved passwords.")
        return
    
    while True:
        print("Please input a website to modify, type 'user' to modify the user credentials, hit 'return' to exit or 'list' to list saved passwords:")
        selection = input("> ").strip().lower()

        if len(selection) < 1:
            print("Modification canceled.")
            break
        
        elif selection == 'list':
            items_per_page(data)
            continue
        
        elif selection == 'user':
            confirmation = input("Type 'username' to change your username or 'password' to change your password:\n")
            if confirmation == 'username':
                new_username = input("Please type your new username:\n")
                while new_username in admin:
                    new_username = input("Username already exists! Please try again or hit 'enter' to exit.\n")
                    if new_username == "":
                        return
                if new_username not in admin:
                    admin[new_username] = admin.pop(current_user)
                    print(f"Username changed successfully from '{current_user}' to '{new_username}'")
            
            if confirmation == 'password':
                new_password = getpass.getpass("Please type your new password:\n")
                while new_password == admin[current_user][0]:
                    new_password = getpass.getpass("This is already your password! Please try again or hit 'enter' to exit.\n")
                    if new_password == "":
                        return
                admin[current_user][0] = new_password
                print(f"Password successfully changed!")
        
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
    command = input("Enter 'next', 'prev', a page number, or hit 'return': ").strip().lower()
    if len(command) < 1:
        return command
    return command

@requires_login
def items_per_page(data): 
    websites = sorted(list(data.items()))
    list_of_dicts = []
    item_range = 20

    # Generate the list_of_dicts with correct slicing
    while websites:
        pages_dict = {}
        for website, password in websites[:item_range]:
            pages_dict[website] = password
        list_of_dicts.append(pages_dict)
        websites = websites[item_range:]

    pages = len(list_of_dicts)
    current_page = 0

    # Print the initial page if it exists
    if pages > 0:
        print(f"Page {current_page + 1}: {list_of_dicts[current_page]}")

    while True:
        command = input("Please input a command, type 'next' to move to the next page, 'prev' to move back a page, a page number to navigate directly or type 'cancel' or hit enter to exit:\n> ")

        if command == "next":
            if current_page < pages - 1:
                current_page += 1
                print(f"Page {current_page + 1}: {list_of_dicts[current_page]}")
            else:
                print("You are already on the last page.")
        elif command == "prev":
            if current_page > 0:
                current_page -= 1
                print(f"Page {current_page + 1}: {list_of_dicts[current_page]}")
            else:
                print("You are already on the first page.")
        elif command.isdigit():
            page_number = int(command) - 1
            if 0 <= page_number < pages:
                current_page = page_number
                print(f"Page {current_page + 1}: {list_of_dicts[current_page]}")
            else:
                print("Invalid page number.")
        elif command == "cancel" or len(command) < 1:
            print("Exiting...")
            return
        else:
            print("Invalid command. Please enter 'next', 'prev', a page number, 'list', 'cancel', or 'return'.")