import tkinter as tk
from tkinter import ttk, messagebox
import data_manager as dm


class FeedbackOverview(tk.Tk):
    def __init__(self, role):
        super().__init__()
        self.title("Feedback Overview")
        self.geometry("1000x600")
        self.FEEDBACK_FILE = "feedback.json"
        self.role = role

        # Predefined options for dropdowns
        self.TYPE_OPTIONS = ["Performance issue", "Bug", "Suggestion"]
        self.STATUS_OPTIONS = ["New", "In Progress", "Resolved", "Closed"]
        self.ASSIGNEE_OPTIONS = ["Jari", "John", "Alexander", "Unassigned"]
        self.PRIORITY_OPTIONS = ['Low', 'Medium', 'High', 'Critical']

        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Create canvas
        self.canvas = tk.Canvas(main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Bind mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Create another frame inside canvas to hold content
        self.feedback_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.feedback_frame, anchor="nw", width=980)

        # Load and display feedback
        self.load_feedback()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_feedback_card(self, parent, title, data, row):
        # Create a frame for each feedback item
        card_frame = ttk.Frame(parent)
        card_frame.grid(row=row, column=0, sticky="ew", padx=10, pady=5)
        parent.grid_columnconfigure(0, weight=1)

        # Title and row configuration
        title_label = ttk.Label(card_frame, text=f"Title: {title}", font=('Arial', 10, 'bold'))
        title_label.grid(row=0, column=0, sticky="w", padx=5)

        # Initialize variables with current values
        priority_value = data.get('priority', 'N/A')
        status_value = data.get('status', 'New')
        type_value = data.get('issue_type', 'N/A')
        assignee_value = data.get('assignee', 'Unassigned')

        # Priority field
        priority_var = tk.StringVar(value=priority_value)
        if self.role in ['qa-tester', 'manager']:
            priority_dropdown = ttk.Combobox(card_frame, textvariable=priority_var,
                                           values=self.PRIORITY_OPTIONS, state="readonly")
            priority_dropdown.set(priority_value)  # Explicitly set the current value
            priority_dropdown.grid(row=0, column=1, sticky="w", padx=5)

            # Update StringVar when a new selection is made
            priority_dropdown.bind('<<ComboboxSelected>>', lambda e: priority_var.set(priority_dropdown.get()))
        else:
            priority_label = ttk.Label(card_frame, text=f"Priority: {priority_value}")
            priority_label.grid(row=0, column=1, sticky="w", padx=5)

        # Status field
        status_var = tk.StringVar(value=status_value)
        if self.role in ['manager', 'developer']:
            status_dropdown = ttk.Combobox(card_frame, textvariable=status_var,
                                         values=self.STATUS_OPTIONS, state="readonly")
            status_dropdown.set(status_value)  # Explicitly set the current value
            status_dropdown.grid(row=0, column=2, sticky="w", padx=5)

            # Update StringVar when a new selection is made
            status_dropdown.bind('<<ComboboxSelected>>', lambda e: status_var.set(status_dropdown.get()))
        else:
            status_label = ttk.Label(card_frame, text=f"Status: {status_value}")
            status_label.grid(row=0, column=2, sticky="w", padx=5)

        # Type field
        type_var = tk.StringVar(value=type_value)
        if self.role in ['qa-tester', 'manager', 'developer']:
            type_dropdown = ttk.Combobox(card_frame, textvariable=type_var,
                                       values=self.TYPE_OPTIONS, state="readonly")
            type_dropdown.set(type_value)  # Explicitly set the current value
            type_dropdown.grid(row=1, column=0, sticky="w", padx=5)

            # Update StringVar when a new selection is made
            type_dropdown.bind('<<ComboboxSelected>>', lambda e: type_var.set(type_dropdown.get()))
        else:
            type_label = ttk.Label(card_frame, text=f"Type: {type_value}")
            type_label.grid(row=1, column=0, sticky="w", padx=5)

        # Assignee field
        assignee_var = tk.StringVar(value=assignee_value)
        if self.role in ['developer', 'manager']:
            assignee_dropdown = ttk.Combobox(card_frame, textvariable=assignee_var,
                                           values=self.ASSIGNEE_OPTIONS, state="readonly")
            assignee_dropdown.set(assignee_value)  # Explicitly set the current value
            assignee_dropdown.grid(row=1, column=1, sticky="w", padx=5, columnspan=2)

            # Update StringVar when a new selection is made
            assignee_dropdown.bind('<<ComboboxSelected>>', lambda e: assignee_var.set(assignee_dropdown.get()))
        else:
            assigned_label = ttk.Label(card_frame, text=f"Assigned to: {assignee_value}")
            assigned_label.grid(row=1, column=1, sticky="w", padx=5, columnspan=2)

        # Submitted by
        submitted_label = ttk.Label(card_frame, text=f"Submitted by: {data.get('submitted_by', 'N/A')}")
        submitted_label.grid(row=2, column=0, sticky="w", padx=5, columnspan=3)

        # Description
        desc_label = ttk.Label(card_frame, text="Description:", font=('Arial', 9, 'bold'))
        desc_label.grid(row=3, column=0, sticky="w", padx=5, pady=(5, 0))

        desc_text = tk.Text(card_frame, height=3, width=80, wrap=tk.WORD)
        desc_text.insert('1.0', data.get('description', 'No description provided'))
        desc_text.config(state='disabled')
        desc_text.grid(row=4, column=0, columnspan=3, sticky="ew", padx=5, pady=(0, 5))

        # Save button for roles with edit permissions
        if self.role in ['developer', 'manager', 'support']:
            save_button = ttk.Button(card_frame, text="Save Changes",
                                   command=lambda t=title, p=priority_var,
                                   s=status_var, tp=type_var,
                                   a=assignee_var: self.save_changes(t, p, s, tp, a))
            save_button.grid(row=5, column=0, columnspan=3, pady=5)

        # Separator
        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(row=row + 1, column=0, sticky="ew", padx=5)

        return card_frame

    def save_changes(self, title, priority_var, status_var, type_var, assignee_var):
        # Load existing feedback data
        feedback_data = dm.load_json(self.FEEDBACK_FILE)

        # Update the specific feedback item
        if title in feedback_data:
            feedback_data[title]['priority'] = priority_var.get()
            feedback_data[title]['status'] = status_var.get()
            feedback_data[title]['issue_type'] = type_var.get()
            feedback_data[title]['assignee'] = assignee_var.get()

            # Print the updated data for this specific item
            print(f"Updated item data: {feedback_data[title]}")

        # Save updated data back to file
        dm.save_json(feedback_data, self.FEEDBACK_FILE)

        # Show a confirmation message
        messagebox.showinfo("Success", f"Changes for '{title}' saved successfully!")

    def load_feedback(self):
        # Load feedback data
        dm.initialize_json_file(self.FEEDBACK_FILE)
        feedback_data = dm.load_json(self.FEEDBACK_FILE)

        # Create a card for each feedback item
        for row, (title, data) in enumerate(feedback_data.items(), start=0):
            self.create_feedback_card(self.feedback_frame, title, data, row * 2)

    def open_overview(self):
        self.mainloop()