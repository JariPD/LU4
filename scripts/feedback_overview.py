import tkinter as tk
from tkinter import ttk
import data_manager as dm


class FeedbackOverview(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Feedback Overview")
        self.geometry("1000x600")
        self.FEEDBACK_FILE = "feedback.json"

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
        parent.grid_columnconfigure(0, weight=1)  # Make the card expand full width

        # Title, Priority, and Status (first row)
        title_label = ttk.Label(card_frame, text=f"Title: {title}", font=('Arial', 10, 'bold'))
        title_label.grid(row=0, column=0, sticky="w", padx=5)

        priority_label = ttk.Label(card_frame, text=f"Priority: {data.get('priority', 'N/A')}")
        priority_label.grid(row=0, column=1, sticky="w", padx=5)

        status_label = ttk.Label(card_frame, text=f"Status: {data.get('status', 'New')}")
        status_label.grid(row=0, column=2, sticky="w", padx=5)

        # Type and Assigned to (second row)
        type_label = ttk.Label(card_frame, text=f"Type: {data.get('issue_type', 'N/A')}")
        type_label.grid(row=1, column=0, sticky="w", padx=5)

        assigned_label = ttk.Label(card_frame, text=f"Assigned to: {data.get('assigned_to', 'Unassigned')}")
        assigned_label.grid(row=1, column=1, sticky="w", padx=5, columnspan=2)

        # Submitted by (third row)
        submitted_label = ttk.Label(card_frame, text=f"Submitted by: {data.get('submitted_by', 'N/A')}")
        submitted_label.grid(row=2, column=0, sticky="w", padx=5, columnspan=3)

        # Description (fourth row)
        desc_label = ttk.Label(card_frame, text="Description:", font=('Arial', 9, 'bold'))
        desc_label.grid(row=3, column=0, sticky="w", padx=5, pady=(5, 0))

        desc_text = tk.Text(card_frame, height=3, width=80, wrap=tk.WORD)
        desc_text.insert('1.0', data.get('description', 'No description provided'))
        desc_text.config(state='disabled')
        desc_text.grid(row=4, column=0, columnspan=3, sticky="ew", padx=5, pady=(0, 5))

        # Separator
        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(row=row + 1, column=0, sticky="ew", padx=5)

        return card_frame

    def load_feedback(self):
        # Load feedback data
        dm.initialize_json_file(self.FEEDBACK_FILE)
        feedback_data = dm.load_json(self.FEEDBACK_FILE)

        # Create a card for each feedback item
        for row, (title, data) in enumerate(feedback_data.items(), start=0):
            self.create_feedback_card(self.feedback_frame, title, data, row * 2)

    def open_overview(self):
        self.mainloop()


# To test the overview page
if __name__ == "__main__":
    overview = FeedbackOverview()
    overview.mainloop()