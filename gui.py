import tkinter as tk
from data_handling import log_entry, update_display, remove_entry

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Entry Logger")

        # Create the data display first
 

        # Create a frame for the log entry widgets on the right
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.label = tk.Label(self.entry_frame, text="Enter Name:")
        self.label.pack()

        # Create the name entry inside the frame
        self.name_entry = tk.Entry(self.entry_frame)
        self.name_entry.pack()

        self.idLabel = tk.Label(self.entry_frame, text="Enter ID number:")
        self.idLabel.pack()

        # Create the ID entry inside the frame
        self.id_entry = tk.Entry(self.entry_frame)
        self.id_entry.pack(padx=10)


        self.items_frame = tk.Frame(self.entry_frame)
        self.items_frame.pack(fill=tk.X, padx=10, pady=10)  # Adjust padding as needed

        
        self.itemLabel = tk.Label(self.items_frame, text="Items being checked out:")
        self.itemLabel.pack(padx=3, pady=5)

        self.keyboard = tk.BooleanVar()
        self.keyboardWidget = tk.Checkbutton(self.items_frame, text="Keyboard", variable=self.keyboard)
        self.keyboardWidget.pack(anchor='w')

        self.mouse = tk.BooleanVar()
        self.mouseWidget = tk.Checkbutton(self.items_frame, text="Mouse", variable=self.mouse)
        self.mouseWidget.pack(anchor='w')

        self.headset = tk.BooleanVar()
        self.headsetWidget = tk.Checkbutton(self.items_frame, text="Headset", variable=self.headset)
        self.headsetWidget.pack(anchor='w')

        self.controller = tk.BooleanVar()
        self.controllerWidget = tk.Checkbutton(self.items_frame, text="Controller", variable=self.controller)
        self.controllerWidget.pack(anchor='w')


        self.checkedframe = tk.Frame(self.root)
        self.checkedframe.pack(fill=tk.X)  # Adjust padding as needed
        self.checkedInLabel = tk.Label(self.checkedframe, text="Students logged in:")
        self.checkedInLabel.pack(padx=3, pady=5)
        self.data_display = tk.Text(self.checkedframe, height=13, width=60)
        self.data_display.pack(side=tk.RIGHT, padx=10, pady=10)

        


        # Create and pack the log button inside the frame
        self.log_button = tk.Button(self.entry_frame, text="Log student", command=self.log)
        self.log_button.pack(padx=10, pady=10)

        # Update the display with current data
        self.update_display()

    def log(self):
        log_entry(self.name_entry.get(), self.id_entry.get(), self.keyboard.get(), self.mouse.get(), self.headset.get(), self.controller.get())
        self.name_entry.delete(0, tk.END)
        self.update_display()

    def update_display(self):
        self.data_display.delete(1.0, tk.END)
        display_text = update_display()
        self.data_display.insert(tk.END, display_text)
