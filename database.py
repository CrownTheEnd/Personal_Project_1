import bcrypt
import math
import csv

file = open("\\wsl.localhost\Ubuntu\home\crowntheend\Boot_dev\Personal_Project_1\database.csv", "r+")
file_info = file.read()
file.write("info")

data = {}

def add_entry(website, password, username="", pin=""):
    data[website] = password, username, pin
    
def delete_entry(): # This is just placeholder.
    pages = (len(websites) // 20) + 1    
    print("Please input a website")
    print(f"Total amount of pages: {pages}")
    
def items_per_page():
    websites = sorted(list(data.items()))
    list_of_dicts = []
    item_range = 20
    pages_dict = {}
    current_page = 0
    pages = (len(websites) // 20) + 1
    
    if len(websites) <= 20:
        print(f"{websites}")
    else:
        for website, password in websites[0:item_range]:
            pages_dict[website] = password
        list_of_dicts.append(pages_dict)
        pages_dict = {}
        item_range += 20
        websites = websites[20:]

    while current_page < pages:
        print(f"Page {current_page + 1}: {list_of_dicts[current_page]}")

        if next_page():
            current_page += 1
        
        if current_page < len(list_of_dicts):
            print(f"Page {current_page + 1}: {list_of_dicts[current_page]}")
    
    # Don't forget to add error handeling
    # Input logic goes here

def next_page():
    state = False
    
    if input() == "next":
        state = True
    
    return state
        
        
    
def page_display(pages):
    
    
    
