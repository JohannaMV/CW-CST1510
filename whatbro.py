import bcrypt

def hash_password(plain_text_pass):
    pass_bytes = plain_text_pass.encode('utf-8')
    salt= bcrypt.gensalt()
    hashed_pass= bcrypt.hashpw(pass_bytes, salt)
    return hashed_pass

def verify_password(plain_text_pass, hashed_pass):
    pass_bytes = plain_text_pass.encode('utf-8')
    hashed_pass_bytes = hashed_pass.encode('utf-8')
    return bcrypt.checkpw(pass_bytes, hashed_pass_bytes)

USER_DATA_FILE = "use.txt"
def register(username, password):
    open(USER_DATA_FILE, "a").close()
    for line in open(USER_DATA_FILE, "r"):
        existing_username = line.strip().split(":")[0]
        if existing_username == username:
            print("Username already exists.")
            return False

    hashed_password = hash_password(password).decode('utf-8')
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username}:{hashed_password}\n")

    print(f"{username} registered")
    return True

def login (username, password):
        with open (USER_DATA_FILE, "r") as file:
            for line in file:
                user, hashed_password= line.strip().split(":",1)
                if user == username:
                    if verify_password(password, hashed_password):
                        print("Login successful")
                        return True
                    else:
                        print("Login failed")
                        return False
        print("Username not found.")
        return False



