# to hash passwords inside passwords.json file
# can take hashed or unhashed passwords
# when you add to JSON file, run this file to keep security

import json
from werkzeug.security import generate_password_hash

json_file_path = 'authentication/passwords.json'

with open(json_file_path, 'r') as f:
    users = json.load(f)

# hash all passwords
for username, password in users.items():
    hashed_password = generate_password_hash(password)
    users[username] = hashed_password  # Replace plain text password with hashed password

# save the hashed passwords back to the JSON file
with open(json_file_path, 'w') as f:
    json.dump(users, f, indent=4)

print("Passwords have been successfully hashed and saved.")
