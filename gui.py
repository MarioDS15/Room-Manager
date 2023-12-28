from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox
from data_handling import log_entry, update_display, remove_entry  # Make sure these are adapted for PyQt

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Room Entry Logger")

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Name entry widgets
        self.name_label = QLabel("Enter Name:")
        self.name_entry = QLineEdit()

        # ID entry widgets
        self.id_label = QLabel("Enter ID number:")
        self.id_entry = QLineEdit()

        # Items being checked out
        self.item_label = QLabel("Items being checked out:")
        self.keyboard_cb = QCheckBox("Keyboard")
        self.mouse_cb = QCheckBox("Mouse")
        self.headset_cb = QCheckBox("Headset")
        self.controller_cb = QCheckBox("Controller")

        # Log student button
        self.log_button = QPushButton("Log student")
        self.log_button.clicked.connect(self.log)

        # Students logged in display
        self.checked_in_label = QLabel("Students logged in:")
        self.data_display = QTextEdit()

        # Layout setup
        self.setup_layouts()

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
