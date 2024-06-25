def write_to_database(data):
    file = open('/home/crowntheend/Boot_dev/Personal_Project_1/database.txt', "w")
    file.write(str(data))
    file.close()
    return True 

def write_to_users(admin):
    file = open('/home/crowntheend/Boot_dev/Personal_Project_1/users.txt', "w")
    file.write(str(admin))
    file.close()
    return True 