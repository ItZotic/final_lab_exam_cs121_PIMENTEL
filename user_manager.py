import os

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def load_users(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        
        users_file = os.path.join('data', 'users.txt')
        if os.path.exists(users_file):
            with open(users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users[username] = password

    def save_users(self):
        users_file = os.path.join('data', 'users.txt')
        with open(users_file, 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username},{password}\n")

    def validate_username(self, username):
        return len(username) >= 4

    def validate_password(self, password):
        return len(password) >= 8

    def register(self, username, password):
        if username in self.users:
            return False, "Username already exists. Please choose another one."
        
        if not self.validate_username(username):
            return False, "Username must be at least 4 characters long."
        if not self.validate_password(password):
            return False, "Password must be at least 8 characters long."

        self.users[username] = password
        self.save_users()
        return True, "Registration successful."

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        return False
