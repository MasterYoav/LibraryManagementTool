import csv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from log_decorator import log_decorator


class UserManager:
    def __init__(self, file_path="csv_files/users.csv"):
        self.file_path = file_path
        self.users = {}  # Stores {username: hashed_password}
        self.load_users()

    def load_users(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.users[row["username"]] = row["password"]

    def save_users(self):
        with open(self.file_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "password"])
            writer.writeheader()
            for username, hashed_password in self.users.items():
                writer.writerow({"username": username, "password": hashed_password})

    @log_decorator("Registered successfully")
    def register_user(self, username, password):
        if username in self.users:
            raise ValueError("Username already exists")
        hashed_password = generate_password_hash(password)
        self.users[username] = hashed_password
        self.save_users()

    @log_decorator("Logged in successfully")
    def authenticate_user(self, username: str, password: str) -> bool:
        hashed_password = self.users.get(username)
        if not hashed_password:
            return False
        return check_password_hash(hashed_password, password)

