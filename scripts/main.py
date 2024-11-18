import tkinter as tk
from tkinter import messagebox
import os
import hashlib
import data_manager as dm
import submit_feedback as sf

# Path to the JSON file for storing user credentials
CREDENTIALS_FILE = "credentials.json"
global root

# Validate login credentials
def validate_login(username, password, current_window):
    credentials = dm.load_json(CREDENTIALS_FILE)

    # Check if the user exists
    if username not in credentials:
        messagebox.showerror("Login Failed", "Invalid username or password")
        return

    # Retrieve salt and stored hash for the user
    salt = bytes.fromhex(credentials[username]['salt'])  # Convert hex back to bytes
    stored_hash = credentials[username]['password_hash']

    # Hash the input password with the stored salt
    input_hash = hashlib.sha256(salt + password.encode()).hexdigest()

    if stored_hash == input_hash:  # Check if hashed password matches
        messagebox.showinfo("Login Success", f"Welcome {username}!")
        current_window.destroy()  # Close the login window

        feedback_page = sf.FeedbackPage(username, credentials[username]['role'])
        feedback_page.mainloop()  # Open the feedback page
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Create a new user
def create_user(username, password):
    # Check if fields are not empty
    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty")
        return

    # Load existing credentials
    credentials = dm.load_json(CREDENTIALS_FILE)

    # Check if the user already exists
    if username in credentials:
        messagebox.showerror("Error", f"User '{username}' already exists!")
        return

    # Generate a unique salt for this user
    salt = os.urandom(8)  # 8 bytes of random data
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()

    # Store the hashed password and salt (in hex format) in the JSON file
    credentials[username] = {
        "password_hash": hashed_password,
        "salt": salt.hex(),  # Convert bytes to hex for storage
        "role": "tester"
    }

    dm.save_json(credentials, CREDENTIALS_FILE)
    messagebox.showinfo("Success", f"User '{username}' has been created successfully!")
    validate_login(username, password, root)


# Run the login app
def run_login_app():
    dm.initialize_json_file(CREDENTIALS_FILE)  # Ensure the credentials file is ready

    # Initialize the main window
    global root
    root = tk.Tk()
    root.title("Login Screen")
    root.geometry("300x250")

    # Username label and entry
    tk.Label(root, text="Username").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    # Password label and entry
    tk.Label(root, text="Password").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    # Login button
    login_button = tk.Button(root, text="Login",
                              command=lambda: validate_login(username_entry.get(), password_entry.get(), root))

    login_button.pack(pady=5)

    # Create user button
    create_user_button = tk.Button(root, text="Create User",
                                    command=lambda: create_user(username_entry.get(), password_entry.get()))

    create_user_button.pack(pady=5)

    # Run the application
    root.mainloop()

# Run the application
if __name__ == "__main__":
    run_login_app()
