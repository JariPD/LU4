import tkinter as tk
from tkinter import ttk, messagebox
import data_manager as dm

class FeedbackPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Beta tester page")
        self.FEEDBACK_FILE = "feedback.json"

        # Create issue_type dropdown
        self.issue_type = tk.StringVar()
        self.issue_type_dropdown = ttk.Combobox(self, textvariable=self.issue_type, state="readonly")
        self.issue_type_dropdown['values'] = ('Performance issue', 'Bug', 'Suggestion')
        self.issue_type_dropdown.grid(row=0, column=0, padx=10, pady=10)

        # Create priority dropdown
        self.priority = tk.StringVar()
        self.priority_dropdown = ttk.Combobox(self, textvariable=self.priority, state="readonly")
        self.priority_dropdown['values'] = ('High priority', 'Medium priority', 'Low')
        self.priority_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Create title field label
        self.title_field_label = tk.Label(self, text="Give the problem a title")
        self.title_field_label.grid(row=2, column=0, columnspan=2, padx=10, sticky="w")

        # Create the title field
        self.title_field = tk.Text(self, height=1, width=40)
        self.title_field.grid(row=3, column=0, columnspan=2, padx=10, sticky="w")

        # Create text field label
        self.description_field_label = tk.Label(self, text="Describe your feedback:")
        self.description_field_label.grid(row=4, column=0, columnspan=2, padx=10, pady=(5, 0) ,sticky="w")

        # Create the text field
        self.description_field = tk.Text(self, height=5, width=50)
        self.description_field.grid(row=5, column=0, columnspan=2)

        # Create the submit button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_feedback)
        self.submit_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def submit_feedback(self):
        # Set value's
        issue_type = self.issue_type_dropdown.get()
        priority = self.priority_dropdown.get()
        description = self.description_field.get("1.0", "end-1c")
        title = self.title_field.get("1.0", "end-1c")

        # initialize and load file
        dm.initialize_credentials_file(self.FEEDBACK_FILE)
        feedback = dm.load_credentials(self.FEEDBACK_FILE)

        # Fill dictionary
        feedback[title] = {
            "issue_type": issue_type,
            "priority": priority,
            "description": description,
        }

        # Save to JSON
        dm.save_credentials(feedback, self.FEEDBACK_FILE)
        messagebox.showinfo("Feedback submitted", "Succesfully submitted feedback, Thank you!") # TO-DO personalize with name

