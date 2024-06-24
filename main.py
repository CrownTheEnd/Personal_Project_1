import getpass
import database
from database import (data, admin)

def main():
    global admin
    print("Please log in: ")
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
                    rtoken_input = getpass.getpass("Please input the recovery token or hit 'enter' to skip: ")
                    database.add_entry(website_input, password_input, username_input, pin_input, rtoken_input)
        print(f"{data}")

                
    #database.logout()
    
    
if __name__ == "__main__":
    main()