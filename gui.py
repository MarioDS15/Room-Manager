from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox
from data_handling import log_entry, update_display, remove_entry  # Make sure these are adapted for PyQt

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Room Entry Logger")

        # Create and set grid layout
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Name entry widgets
        self.name_label = QLabel("Enter Name:")
        self.name_entry = QLineEdit()
        self.grid_layout.addWidget(self.name_label, 0, 0)
        self.grid_layout.addWidget(self.name_entry, 0, 1)

        # ID entry widgets
        self.id_label = QLabel("Enter ID number:")
        self.id_entry = QLineEdit()
        self.grid_layout.addWidget(self.id_label, 1, 0)
        self.grid_layout.addWidget(self.id_entry, 1, 1)

        # Items being checked out
        self.item_label = QLabel("Items being checked out:")
        self.keyboard_cb = QCheckBox("Keyboard")
        self.mouse_cb = QCheckBox("Mouse")
        self.headset_cb = QCheckBox("Headset")
        self.controller_cb = QCheckBox("Controller")
        self.grid_layout.addWidget(self.item_label, 2, 0)
        self.grid_layout.addWidget(self.keyboard_cb, 3, 0)
        self.grid_layout.addWidget(self.mouse_cb, 4, 0)
        self.grid_layout.addWidget(self.headset_cb, 5, 0)
        self.grid_layout.addWidget(self.controller_cb, 6, 0)

        # Log student button
        self.log_button = QPushButton("Log student")
        self.grid_layout.addWidget(self.log_button, 7, 0, 1, 2)  # Spanning 2 columns

        # Students logged in display
        self.checked_in_label = QLabel("Students logged in:")
        self.data_display = QTextEdit()
        self.grid_layout.addWidget(self.checked_in_label, 8, 0)
        self.grid_layout.addWidget(self.data_display, 9, 0, 1, 2)  # Spanning 2 columns

        # Connect button signal to slot
        self.log_button.clicked.connect(self.log)
    
    def setup_layouts(self):
        # Create horizontal layouts for name and ID entries
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_entry)

        id_layout = QHBoxLayout()
        id_layout.addWidget(self.id_label)
        id_layout.addWidget(self.id_entry)

        # Create a vertical layout for checkboxes
        items_layout = QVBoxLayout()
        items_layout.addWidget(self.item_label)
        items_layout.addWidget(self.keyboard_cb)
        items_layout.addWidget(self.mouse_cb)
        items_layout.addWidget(self.headset_cb)
        items_layout.addWidget(self.controller_cb)

        # Add name, ID, items, and log button to the main layout
        self.main_layout.addLayout(name_layout)
        self.main_layout.addLayout(id_layout)
        self.main_layout.addLayout(items_layout)
        self.main_layout.addWidget(self.log_button)
        
        # Add the logged-in label and text display to the main layout
        self.main_layout.addWidget(self.checked_in_label)
        self.main_layout.addWidget(self.data_display)

    def log(self):
        name = self.name_entry.text()
        id_number = self.id_entry.text()
        keyboard = self.keyboard_cb.isChecked()
        mouse = self.mouse_cb.isChecked()
        headset = self.headset_cb.isChecked()
        controller = self.controller_cb.isChecked()

        # Assuming log_entry function is adapted for PyQt
        log_entry(name, id_number, keyboard, mouse, headset, controller)
        self.name_entry.clear()
        self.update_display()

    def update_display(self):
        self.data_display.delete(1.0, tk.END)
        display_text = update_display()
        self.data_display.insert(tk.END, display_text)
