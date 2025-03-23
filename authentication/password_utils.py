# used in app.py to verify password during sign in

import json
from werkzeug.security import check_password_hash

# where hashed passwords are saved
json_file_path = 'authentication/passwords.json'

def check_user_credentials(username, password):
    try:

        with open(json_file_path, 'r') as f:
            users = json.load(f)
            print(users)
        
            # check if the username exists
            if username in users:
                print(username)

                # get the hashed password from the file
                stored_hash = users[username]
                
                # check if the entered password matches the stored hash
                if check_password_hash(stored_hash, password):
                    return True  # Password is correct
                else:
                    return False  # Incorrect password
            else:
                return False  # Username not found
            
    except FileNotFoundError:
        return False  # JSON file not found, return False



