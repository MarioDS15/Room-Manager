import tkinter as tk
from data_handling import log_entry, update_display, remove_entry

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Entry Logger")

        # Create and pack labels and entry fields

        self.log_button = tk.Button(self.root, text="Log Entry", command=self.log)
        self.log_button.pack()

        self.data_display = tk.Text(self.root, height=10, width=40)
        self.data_display.pack()

        self.update_display()

    def log(self):
        log_entry(self.name_entry.get())
        self.name_entry.delete(0, tk.END)
        self.update_display()

    def update_display(self):
        self.data_display.delete(1.0, tk.END)
        display_text = update_display()
        self.data_display.insert(tk.END, display_text)

    def remove(self, index):
        remove_entry(index)
        self.update_display()