import tkinter as tk
from tkinter import messagebox

# Dictionary of valid usernames and passwords
valid_credentials = {
    "user": "pass",
    "qa-tester": "pass",
    "manager": "pass",
    "developer": "pass"
}

# Function to validate login credentials
def validate_login(username, password):
    # Check if the username exists in the dictionary and if the password matches
    if valid_credentials.get(username) == password:
        messagebox.showinfo("Login Success", f"Welcome {username}!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Example of how to use the function in a tkinter application
def run_login_app():
    # Initialize the main window
    root = tk.Tk()
    root.title("Login Screen")
    root.geometry("300x200")

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
                             command=lambda: validate_login(username_entry.get(), password_entry.get()))
    login_button.pack(pady=10)

    # Run the application
    root.mainloop()

# Run the login application
run_login_app()