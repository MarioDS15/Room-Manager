from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QListWidget, QListWidgetItem, QMessageBox, QToolBar
from PyQt5.QtCore import Qt, QTimer
from room_variables import *
from data_handling import *
from data_loader import *

class EditItemsWindow(QMainWindow):
    def __init__(self, name, id, dict):
        super().__init__()
        self.setWindowTitle('Edit Items Window')
        self.setMinimumSize(300, 500)
        self.setFixedSize(500, 500)

        self.name = name
        self.id = id
        self.dict = dict
        # Create and set grid layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QGridLayout(central_widget)

        # Data entry nested grid layout
        self.dataWidget = QWidget()
        self.item_layout = QGridLayout(self.dataWidget)
        self.main_layout.addWidget(self.dataWidget, 1, 0)

        self.title_label = QLabel("Edit student items")
        self.main_layout.addWidget(self.title_label, 0, 0, Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        self.dataEntryGUI()

    def dataEntryGUI(self):
        """
        Creates the GUI for the room settings window"""
        label = QLabel(f"{self.name} [{self.id}] has the following items checked out:")
        self.main_layout.addWidget(label, 1, 0, Qt.AlignCenter)

        self.keyboard = QCheckBox("Keyboard")
        self.keyboard.setChecked(self.dict['Keyboard'])
        self.main_layout.addWidget(self.keyboard, 2, 0, Qt.AlignCenter)

        self.mouse = QCheckBox("Mouse")
        self.mouse.setChecked(self.dict['Mouse'])
        self.main_layout.addWidget(self.mouse, 3, 0, Qt.AlignCenter)

        self.mousepad = QCheckBox("Mousepad")
        self.mousepad.setChecked(self.dict['Mousepad'])
        self.main_layout.addWidget(self.mousepad, 4, 0, Qt.AlignCenter)

        self.headset = QCheckBox("Headset")
        self.headset.setChecked(self.dict['Headset'])
        self.main_layout.addWidget(self.headset, 5, 0, Qt.AlignCenter)

        self.controller = QCheckBox("Controller")
        self.controller.setChecked(self.dict['Controller'])
        self.main_layout.addWidget(self.controller, 6, 0, Qt.AlignCenter)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.main_layout.addWidget(self.submit_button, 7, 0, Qt.AlignCenter)

    def submit(self):
        """Updates the items datasheet in accordance if its been checked out/returned
        """
        self.dict['Keyboard'] = self.keyboard.isChecked()
        self.dict['Mouse'] = self.mouse.isChecked()
        self.dict['Mousepad'] = self.mousepad.isChecked()
        self.dict['Headset'] = self.headset.isChecked()
        self.dict['Controller'] = self.controller.isChecked()
        currentInv = items_to_dict(CURRENT_STUDENTS_FILE, self.id)
        if currentInv is not None:
            if self.dict['Keyboard'] == False and currentInv['Keyboard'] == True:
                set_keyboard_in_use(get_keyboard_in_use() - 1)
            elif self.dict['Keyboard'] == True and currentInv['Keyboard'] == False:
                set_keyboard_in_use(get_keyboard_in_use() + 1)
            
            if self.dict['Mouse'] == False and currentInv['Mouse'] == True:
                set_mouse_in_use(get_mouse_in_use() - 1)
            elif self.dict['Mouse'] == True and currentInv['Mouse'] == False:
                set_mouse_in_use(get_mouse_in_use() + 1)

            if self.dict['Mousepad'] == False and currentInv['Mousepad'] == True:
                set_mousepad_in_use(get_mousepad_in_use() - 1)
            elif self.dict['Mousepad'] == True and currentInv['Mousepad'] == False:
                set_mousepad_in_use(get_mousepad_in_use() + 1)
            
            if self.dict['Headset'] == False and currentInv['Headset'] == True:
                set_headset_in_use(get_headset_in_use() - 1)
            elif self.dict['Headset'] == True and currentInv['Headset'] == False:
                set_headset_in_use(get_headset_in_use() + 1)
            
            if self.dict['Controller'] == False and currentInv['Controller'] == True:
                set_controller_in_use(get_controller_in_use() - 1)
            elif self.dict['Controller'] == True and currentInv['Controller'] == False:
                set_controller_in_use(get_controller_in_use() + 1)
        update_dict(CURRENT_STUDENTS_FILE, self.id, self.dict)
        self.close()
