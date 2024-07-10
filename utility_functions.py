import random
import json
import bcrypt
import zipfile
import pyzipper
import os
from io import BytesIO


"""def write_to_database(data):
    file = open('/home/crowntheend/Boot_dev/Personal_Project_1/database.txt', "w")
    file.write(str(data))
    file.close()
    return True """

def write_to_users(admin):
    file = open('/home/crowntheend/Boot_dev/Personal_Project_1/users.txt', "w")
    file.write(str(admin))
    file.close()
    return True

def generate_token(length):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    token = ''.join(random.choice(characters) for _ in range(length))
    return token

def hash_password(password: str) -> bytes:
    """
    Hashes a plain-text password using bcrypt.
    
    Args:
    password (str): The plain-text password to hash.
    
    Returns:
    bytes: The hashed password.
    """
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed

def check_password(plain_password: str, hashed_password: bytes) -> bool:
    """
    Checks a plain-text password against a hashed password.
    
    Args:
    plain_password (str): The plain-text password to check.
    hashed_password (bytes): The hashed password to compare against.
    
    Returns:
    bool: True if the password matches, False otherwise.
    """
    plain_password_bytes = plain_password.encode('utf-8')
    return bcrypt.checkpw(plain_password_bytes, hashed_password)

"""def write_to_database(input_string, password, zip_path="/home/crowntheend/Boot_dev/Personal_Project_1/database.zip"):
    # Create a BytesIO object to hold the file content
    byte_data = BytesIO(str(input_string).encode())
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add the BytesIO content to the zip file
        zip_info = zipfile.ZipInfo("file.txt")  # You can name it anything you like
        zipf.writestr(zip_info, byte_data.getvalue())
        # Set the password for the zip file
        zipf.setpassword(password.encode())

def read_zip(password, zip_path="/home/crowntheend/Boot_dev/Personal_Project_1/database.zip"):

    if not os.path.exists(zip_path) or os.path.getsize(zip_path) == 0:
        file = open(zip_path, "w")
        file.close()
        return ""
    
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.setpassword(password.encode())
        file_name = zipf.namelist()[0]
        with zipf.open(file_name) as file:
            content = file.read().decode()
    return content"""

def write_to_database(data, password, zip_path):
    # Convert the dictionary to a JSON string and then to bytes
    input_string = json.dumps(data).encode('utf-8')
    
    # Create a BytesIO object to hold the zip content
    byte_data = BytesIO()

    # Write the string to the zip file in memory
    with pyzipper.AESZipFile(byte_data, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
        zipf.setpassword(password.encode('utf-8'))
        zipf.writestr('file.txt', input_string)

    # Write the in-memory zip file to the actual file
    with open(zip_path, 'wb') as f:
        f.write(byte_data.getvalue())

def read_zip(password, zip_path):
    if not os.path.exists(zip_path) or os.path.getsize(zip_path) == 0:
        file = open(zip_path, "w")
        file.close()
        return ""

    with pyzipper.AESZipFile(zip_path, 'r', encryption=pyzipper.WZ_AES) as zipf:
        zipf.setpassword(password.encode('utf-8'))
        file_name = zipf.namelist()[0]
        with zipf.open(file_name) as file:
            content = file.read().decode('utf-8')
    return content