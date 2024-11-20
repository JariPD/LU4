import tkinter as tk
from tkinter import messagebox
import os
import hashlib
import data_manager as dm
import submit_feedback as sf

class LoginApp:
    def __init__(self):
        self.CREDENTIALS_FILE = "credentials.json"
        self.root = None

    def validate_login(self, username, password, current_window):
        """Validate login with giving data from entry fields"""
        credentials = dm.load_json(self.CREDENTIALS_FILE)

        # Check if the user exists
        if username not in credentials:
            messagebox.showerror("Login Failed", "Invalid username or password")
            return

        # Retrieve salt and stored hash for the user
        salt = bytes.fromhex(credentials[username]['salt'])
        stored_hash = credentials[username]['password_hash']

        # Hash the input password with the stored salt
        input_hash = hashlib.sha256(salt + password.encode()).hexdigest()

        if stored_hash == input_hash:
            messagebox.showinfo("Login Success", f"Welcome {username}!")
            current_window.destroy()

            feedback_page = sf.FeedbackPage(username, credentials[username]['role'])
            feedback_page.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_user(self, username, password):
        """Create a new user with given credentials"""
        # Check if fields are not empty
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return

        # Load existing credentials
        credentials = dm.load_json(self.CREDENTIALS_FILE)

        # Check if the user already exists
        if username in credentials:
            messagebox.showerror("Error", f"User '{username}' already exists!")
            return

        # Generate a unique salt for this user
        salt = os.urandom(8)
        hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()

        # Store the hashed password and salt (in hex format) in the JSON file
        credentials[username] = {
            "password_hash": hashed_password,
            "salt": salt.hex(),
            "role": "tester"
        }

        dm.save_json(credentials, self.CREDENTIALS_FILE)
        messagebox.showinfo("Success", f"User '{username}' has been created successfully!")
        self.validate_login(username, password, self.root)

    def run(self):
        dm.initialize_json_file(self.CREDENTIALS_FILE)

        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Login Screen")
        self.root.geometry("300x250")

        # Username label and entry
        tk.Label(self.root, text="Username").pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        # Password label and entry
        tk.Label(self.root, text="Password").pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        # Login button
        login_button = tk.Button(
            self.root,
            text="Login",
            command=lambda: self.validate_login(
                username_entry.get(),
                password_entry.get(),
                self.root
            )
        )
        login_button.pack(pady=5)

        # Create user button
        create_user_button = tk.Button(
            self.root,
            text="Create User",
            command=lambda: self.create_user(
                username_entry.get(),
                password_entry.get()
            )
        )
        create_user_button.pack(pady=5)

        # Run the application
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    login_app = LoginApp()
    login_app.run()