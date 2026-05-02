# Multi User Authentication System
# Python Internship Task

import json
import os
import re
import hashlib
import uuid
from datetime import datetime

DATA_FILE = "users.json"
MAX_ATTEMPTS = 3
MIN_PASS_LEN = 8


def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, stored_hash):
    return hash_password(password) == stored_hash


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None


def is_strong_password(password):
    if len(password) < MIN_PASS_LEN:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Add at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Add at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Add at least one number"
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>_\-]', password):
        return False, "Add at least one special character"
    return True, ""


def input_required(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required.")


def print_header(title):
    print("\n" + "-" * 50)
    print(title)
    print("-" * 50)


def print_users(users):
    if not users:
        print("No users found.")
        return

    print("\nUsername        Email                     Role    Status")
    print("-" * 60)

    for username, data in users.items():
        status = "Locked" if data.get("locked") else "Active"
        print(f"{username:<15} {data['email']:<25} {data['role']:<7} {status}")

    print("-" * 60)


# Register
def register(users):
    print_header("Register")

    while True:
        username = input_required("Username: ")
        if username in users:
            print("Username already exists.")
        elif len(username) < 3:
            print("Username too short.")
        else:
            break

    while True:
        email = input_required("Email: ")
        if not is_valid_email(email):
            print("Invalid email.")
            continue
        if any(u["email"].lower() == email.lower() for u in users.values()):
            print("Email already used.")
        else:
            break

    while True:
        password = input_required("Password: ")
        valid, msg = is_strong_password(password)
        if not valid:
            print(msg)
            continue

        confirm = input_required("Confirm Password: ")
        if password != confirm:
            print("Passwords do not match.")
        else:
            break

    role = "Admin" if not users else "User"

    users[username] = {
        "id": str(uuid.uuid4()),
        "email": email,
        "password_hash": hash_password(password),
        "role": role,
        "joined_on": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "failed_attempts": 0,
        "locked": False
    }

    save_users(users)
    print(f"Account created for {username} ({role})")


# Login
def login(users):
    print_header("Login")

    identifier = input_required("Username or Email: ")
    password = input_required("Password: ")

    username = None

    if identifier in users:
        username = identifier
    else:
        for u, data in users.items():
            if data["email"].lower() == identifier.lower():
                username = u
                break

    if not username:
        print("User not found.")
        return None

    user = users[username]

    if user.get("locked"):
        print("Account is locked.")
        return None

    if verify_password(password, user["password_hash"]):
        user["failed_attempts"] = 0
        save_users(users)
        print(f"Welcome {username}")
        return username
    else:
        user["failed_attempts"] += 1

        if user["failed_attempts"] >= MAX_ATTEMPTS:
            user["locked"] = True
            print("Account locked due to too many attempts.")
        else:
            remaining = MAX_ATTEMPTS - user["failed_attempts"]
            print(f"Wrong password. {remaining} attempts left.")

        save_users(users)
        return None


# Reset password
def reset_password(users, current_user=None):
    print_header("Reset Password")

    if current_user:
        username = current_user
    else:
        username = input_required("Username: ")
        if username not in users:
            print("User not found.")
            return

        email = input_required("Email: ")
        if users[username]["email"].lower() != email.lower():
            print("Email does not match.")
            return

    while True:
        new_pass = input_required("New Password: ")
        valid, msg = is_strong_password(new_pass)
        if not valid:
            print(msg)
            continue

        confirm = input_required("Confirm Password: ")
        if new_pass != confirm:
            print("Passwords do not match.")
        else:
            break

    users[username]["password_hash"] = hash_password(new_pass)
    users[username]["failed_attempts"] = 0
    users[username]["locked"] = False

    save_users(users)
    print("Password updated.")


# Delete account
def delete_account(users, current_user):
    print_header("Delete Account")

    confirm = input("Type your username to confirm: ")

    if confirm != current_user:
        print("Cancelled.")
        return False

    password = input_required("Password: ")

    if not verify_password(password, users[current_user]["password_hash"]):
        print("Wrong password.")
        return False

    del users[current_user]
    save_users(users)

    print("Account deleted.")
    return True


# Admin panel
def admin_panel(users, current_user):
    while True:
        print_header("Admin Panel")

        print("1. View Users")
        print("2. Unlock User")
        print("3. Delete User")
        print("4. Change Role")
        print("0. Back")

        choice = input("Choice: ")

        if choice == "1":
            print_users(users)

        elif choice == "2":
            username = input_required("Username: ")
            if username in users:
                users[username]["locked"] = False
                users[username]["failed_attempts"] = 0
                save_users(users)
                print("Unlocked.")
            else:
                print("User not found.")

        elif choice == "3":
            username = input_required("Username: ")
            if username in users and username != current_user:
                del users[username]
                save_users(users)
                print("Deleted.")
            else:
                print("Invalid user.")

        elif choice == "4":
            username = input_required("Username: ")
            if username in users:
                users[username]["role"] = "Admin" if users[username]["role"] == "User" else "User"
                save_users(users)
                print("Role updated.")
            else:
                print("User not found.")

        elif choice == "0":
            break

        input("Press Enter...")


# User menu
def user_menu(users, username):
    while True:
        user = users[username]

        print_header(f"{username} ({user['role']})")

        print("1. View Profile")
        print("2. Reset Password")
        print("3. Delete Account")
        if user["role"] == "Admin":
            print("4. Admin Panel")
        print("0. Logout")

        choice = input("Choice: ")

        if choice == "1":
            print(f"\nUsername: {username}")
            print(f"Email: {user['email']}")
            print(f"Role: {user['role']}")
            print(f"Joined: {user['joined_on']}")
            print(f"Status: {'Locked' if user['locked'] else 'Active'}")

        elif choice == "2":
            reset_password(users, username)

        elif choice == "3":
            if delete_account(users, username):
                return

        elif choice == "4" and user["role"] == "Admin":
            admin_panel(users, username)

        elif choice == "0":
            print("Logged out.")
            return

        else:
            print("Invalid option.")

        input("Press Enter...")


def main_menu():
    print("""
1. Register
2. Login
3. Reset Password
0. Exit
""")


def main():
    users = load_users()
    print(f"Users loaded: {len(users)}")

    while True:
        main_menu()
        choice = input("Select: ")

        try:
            if choice == "1":
                register(users)

            elif choice == "2":
                user = login(users)
                if user:
                    user_menu(users, user)

            elif choice == "3":
                reset_password(users)

            elif choice == "0":
                print("Goodbye.")
                break

            else:
                print("Invalid option.")

        except KeyboardInterrupt:
            print("\nInterrupted.")
        except Exception as e:
            print(f"Error: {e}")

        input("\nPress Enter...")


if __name__ == "__main__":
    main()