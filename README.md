Password manager


Database will store "website = password" key=value pairs (probably with a dictionary).

Would be cool to have a basic front end for it, maybe like a login and password on the first page and then a list of entries with a search bar.

Setup process to guide a new user.
    An if check to see if it's the first time the .exe has been run and set a variable to False after.
    If True then the setup process starts, prompting a username and password and generating a recovery key for forgotten passwords.
    If False then prompts login and then proceeds to the next step of functions.
    Maybe a command bar for admin tools?


Admin tools:
    Requires login and password to access.
    Editing entries, add/modify/delete.
        Add/modify functions would require a key=value pair
        Delete would just require a key
    Maybe failsafe "purge" command to empty the database with a VERY explicit warning.
    Command to print all entries to a LOCKED zip text file.
        Maybe an option to overwrite or generate a new one.
        Find a format for how the file is named for cases when a new file is generated.


MAKE SURE TO ENCRYPT THE DATABASE FOR PRIVACY

Possible libraries to use:
    cryptography: for encrypting the database
    pyminizip: for creating locked zip files
    zipfile module: for creating zips
    bcrypt: for Hashing Passwords
    sqlite3: for local database (you query it with the sql language)
        SELECT * FROM passwords
        WHERE password = 'testing123';
    