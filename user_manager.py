import os

class UserManager:
    def __init__(personal):
        personal.users = {} 

    def load_users(personal):
        if not os.path.exists('data'):
            os.makedirs('data')
        
        users_file = os.path.join('data', 'users.txt')
        if os.path.exists(users_file):
            with open(users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    personal.users[username] = password

    def save_users(personal):
        users_file = os.path.join('data', 'users.txt')
        with open(users_file, 'w') as file:
            for username, password in personal.users.items():
                file.write(f"{username},{password}\n")

    def validate_username(personal, username):
        if len(username) < 4:
            return False
        return True

    def validate_password(personal, password):
        if len(password) < 8:
            return False
        return True

    def register(personal, username, password):
        if username in personal.users:
            return False, "Username already exists. Please choose another one."
        
        if not personal.validate_username(username):
            return False, "Username must be at least 4 characters long."
        if not personal.validate_password(password):
            return False, "Password must be at least 8 characters long."

        personal.users[username] = password
        personal.save_users()
        return True, "Registration successful."

    def login(personal, username, password):
        if username in personal.users and personal.users[username] == password:
            return True, "Login successful."
        else:
            return False, "Invalid username or password."
