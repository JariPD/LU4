import tkinter as tk
from tkinter import ttk, messagebox
import scripts.data_manager as dm

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

        # Priority order for sorting
        self.PRIORITY_ORDER = {
            'Critical': 0,
            'High': 1,
            'Medium': 2,
            'Low': 3,
            'N/A': 4  # Default priority for items without priority
        }

        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Create sorting controls frame
        sort_frame = ttk.Frame(main_frame)
        sort_frame.pack(fill=tk.X, padx=10, pady=5)

        # Add sort direction toggle
        self.sort_ascending = tk.BooleanVar(value=True)
        sort_direction_btn = ttk.Button(
            sort_frame,
            text="Toggle Sort Direction",
            command=self.toggle_sort_direction
        )
        sort_direction_btn.pack(side=tk.LEFT, padx=5)

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

    def toggle_sort_direction(self):
        """Toggle between ascending and descending sort order"""
        self.sort_ascending.set(not self.sort_ascending.get())
        self.refresh_feedback()

    def sort_feedback_by_priority(self, feedback_data):
        """
        Sort feedback items by priority, handling cases where priority is not set
        or is invalid.
        """

        def get_priority_order(item):
            # Extract priority from the feedback item, defaulting to 'N/A' if not found
            priority = item[1].get('priority', 'N/A')

            # If priority is None or not in our priority order, treat it as 'N/A'
            if priority not in self.PRIORITY_ORDER:
                priority = 'N/A'

            return (
                self.PRIORITY_ORDER[priority],  # Primary sort by priority
                item[0].lower()  # Secondary sort by title
            )

        sorted_items = sorted(
            feedback_data.items(),
            key=get_priority_order,
            reverse=not self.sort_ascending.get()
        )
        return dict(sorted_items)

    def refresh_feedback(self):
        """Clear and reload all feedback items"""
        # Clear existing feedback cards
        for widget in self.feedback_frame.winfo_children():
            widget.destroy()

        # Reload feedback
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
        desc_text.grid(row=4, column=0, columnspan=3, sticky="ew", padx=5, pady=(0, 5))

        # Add buttons frame
        buttons_frame = ttk.Frame(card_frame)
        buttons_frame.grid(row=5, column=0, columnspan=3, pady=5)

        # Save button for roles with edit permissions
        save_button = ttk.Button(buttons_frame, text="Save Changes",
                                     command=lambda t=title, p=priority_var,
                                                    s=status_var, tp=type_var,
                                                    a=assignee_var, d=desc_text: self.save_changes(t, p, s, tp, a, d))
        save_button.pack(side=tk.LEFT, padx=5)

        # Add remove button for managers only
        if self.role in ['qa-tester', 'manager']:
            remove_button = ttk.Button(buttons_frame, text="Remove Feedback",
                                           command=lambda t=title, cf=card_frame: self.remove_feedback(t, cf))
            remove_button.pack(side=tk.LEFT, padx=5)

        # Separator
        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(row=row + 1, column=0, sticky="ew", padx=5)

        return card_frame

    def save_changes(self, title, priority_var, status_var, type_var, assignee_var, desc_text):
        # Load existing feedback data
        feedback_data = dm.load_json(self.FEEDBACK_FILE)

        # Get the current data for the specific feedback item
        current_data = feedback_data.get(title, {})

        # Update the specific feedback item with role-based permissions
        update_data = current_data.copy()

        # Priority can only be edited by manager or qa-tester
        if self.role in ['manager', 'qa-tester']:
            update_data['priority'] = priority_var.get()

        # Status can only be edited by manager or developer
        if self.role in ['manager', 'developer']:
            update_data['status'] = status_var.get()

        # Type can be edited by manager, qa-tester, and developer
        if self.role in ['manager', 'qa-tester', 'developer']:
            update_data['issue_type'] = type_var.get()

        # Assignee can only be edited by manager or developer
        if self.role in ['manager', 'developer']:
            update_data['assignee'] = assignee_var.get()

        # Always allow description update
        update_data['description'] = desc_text.get('1.0', 'end-1c')

        # Update the specific feedback item
        feedback_data[title] = update_data

        # Save updated data back to file
        dm.save_json(feedback_data, self.FEEDBACK_FILE)

        # Show a confirmation message
        messagebox.showinfo("Success", f"Changes for '{title}' saved successfully!")

        # Refresh the display to show the new sort order
        self.refresh_feedback()

    def load_feedback(self):
        # Load feedback data
        dm.initialize_json_file(self.FEEDBACK_FILE)
        feedback_data = dm.load_json(self.FEEDBACK_FILE)

        # Sort feedback data by priority
        sorted_feedback = self.sort_feedback_by_priority(feedback_data)

        # Create a card for each feedback item
        for row, (title, data) in enumerate(sorted_feedback.items(), start=0):
            self.create_feedback_card(self.feedback_frame, title, data, row * 2)

    def remove_feedback(self, title, card_frame):
        # Show confirmation dialog
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to remove the feedback titled '{title}'?\nThis action cannot be undone.",
            icon='warning'
        )

        if confirm:
            try:
                # Load current feedback data
                feedback_data = dm.load_json(self.FEEDBACK_FILE)

                # Remove the feedback from the data
                if title in feedback_data:
                    del feedback_data[title]

                    # Save updated data
                    dm.save_json(feedback_data, self.FEEDBACK_FILE)

                    # Remove the card from the UI
                    card_frame.grid_remove()

                    # Show success message
                    messagebox.showinfo("Success", f"Feedback '{title}' has been removed successfully!")

                    # Refresh the UI to prevent layout issues
                    self.feedback_frame.update_idletasks()
                else:
                    messagebox.showerror("Error", f"Feedback '{title}' not found in stored data.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while removing the feedback: {str(e)}")


    def open_overview(self):
        self.mainloop()