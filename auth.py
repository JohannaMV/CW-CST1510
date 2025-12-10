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

USER_DATA_FILE = "DATA/users.txt"

def register_user(username, password, role= "user"):
    open(USER_DATA_FILE, "a").close()
    for line in open(USER_DATA_FILE, "r"):
        existing_username = line.strip().split(":")[0]
        if existing_username == username:
            print("Username already exists.")
            return False

    hashed_password = hash_password(password).decode('utf-8')
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username}:{hashed_password}:{role}\n")

    print(f"{username} registered")
    return True

def login(username, password):
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) != 3:
                continue  # skip invalid lines

            user, hashed_password, role = parts

            if user == username:
                if verify_password(password, hashed_password):
                    print("Login successful")
                    return True
                else:
                    print("Login failed")
                    return False

    print("Username not found.")
    return False

def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    return True, ""

def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""

def display_menu():
    """displays menu options"""
    print("\n" + "="*50)
    print("     MULTI-DOMAIN INTELLIGENCE PLATFORM   ")
    print("     Secure Authentication System      ")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """main program loop"""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice=input("\nPlease select an option(1-3): ").strip()

        if choice == "1":
            #registration
            print("\n     USER REGISTRATION    ")
            username= input("Enter username: ").strip()

            #validate user
            is_valid, error_msg= validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password= input("Enter password: ").strip()

            #validate pw
            is_valid, error_msg= validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            #confirm pw
            password_confirm= input("confirm password: ").strip()
            if password != password_confirm:
                print("ERROR: Passwords do not match.")
                continue

            #inserts role
            role = input("Enter role (user/admin): ").strip().lower()
            if role not in ["user", "admin"]:
                role = "user"

            #register user
            register_user(username, password, role)

        elif choice == "2":
            #login
            print("\n     USER LOGIN    ")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            #attempt login
            if login(username, password):
                print("\nYou are now logged in.")

                input("\nPress enter to return to the main menu...")
        elif choice == "3":
            #exit
            print("\nThank you for using the authentication system.")
            print("\n     EXIT    ")
            break
        else:
            print("\nError: Invalid input.")

if __name__ == "__main__":
    main()

