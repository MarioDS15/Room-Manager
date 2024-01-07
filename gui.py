from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from data_handling import *
from datetime import datetime, timedelta

import csv
import sys

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #self.theme()
        self.setWindowTitle("Room Entry Logger")

        # Create and set grid layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QGridLayout(central_widget)

        # Data entry nested grid layout
        self.dataWidget = QWidget()
        self.data_layout = QGridLayout(self.dataWidget)
        self.main_layout.addWidget(self.dataWidget, 0, 0)

        self.title_label = QLabel("Room Entry Logger")
        self.title_label.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        self.data_layout.addWidget(self.title_label, 0, 0, 1, 2)

        self.dataEntryGUI()
        self.itemEntryGUI()
        self.checkedInGUI()
        self.timeoutGUI()

        self.populate()
        self.populateTimeout()
        

    def dataEntryGUI(self):
        # Name entry widgets
        self.name_label = QLabel("Enter Name")
        self.name_entry = QLineEdit()
        self.data_layout.addWidget(self.name_label, 1, 0)
        self.data_layout.addWidget(self.name_entry, 1, 1)

        # ID entry widgets
        self.id_label = QLabel("Enter ID number")
        self.id_entry = QLineEdit()
        self.data_layout.addWidget(self.id_label, 2, 0)
        self.data_layout.addWidget(self.id_entry, 2, 1)

        # Log student button
        self.log_button = QPushButton("Log student")
        self.data_layout.addWidget(self.log_button, 3, 0, 2, 2)  # Spanning 2 columns
        self.log_button.clicked.connect(self.log)
        pass

    def itemEntryGUI(self):
        # Item entry nested grid layout
        self.itemWidget = QWidget()
        self.item_layout = QGridLayout(self.itemWidget)
        self.main_layout.addWidget(self.itemWidget, 0, 1)

        # Items being checked out
        self.item_label = QLabel("Items being checked out")
        self.keyboard_cb = QCheckBox("Keyboard")
        self.mouse_cb = QCheckBox("Mouse")
        self.headset_cb = QCheckBox("Headset")
        self.controller_cb = QCheckBox("Controller")
        self.mousepad_cb = QCheckBox("Mousepad")
        self.item_layout.addWidget(self.item_label, 2, 0)
        self.item_layout.addWidget(self.keyboard_cb, 3, 0)
        self.item_layout.addWidget(self.mouse_cb, 4, 0)
        self.item_layout.addWidget(self.headset_cb, 5, 0)
        self.item_layout.addWidget(self.controller_cb, 6, 0)
        self.item_layout.addWidget(self.mousepad_cb, 7, 0)


    def checkedInGUI(self):
        # Checked in students 
        self.checkedInWidget = QWidget()
        self.checkedInlayout = QGridLayout(self.checkedInWidget)
        self.main_layout.addWidget(self.checkedInWidget, 1, 0)

        # Students logged in display
        self.checked_in_label = QLabel("Students logged in")
        self.checkedInList = QListWidget()
        self.checkedInlayout.addWidget(self.checked_in_label, 0, 0)
        self.checkedInlayout.addWidget(self.checkedInList, 1, 0, 1, 1)

    def timeoutGUI(self):
        self.timeoutWidget = QWidget()
        self.timeoutlayout = QGridLayout(self.timeoutWidget)
        self.main_layout.addWidget(self.timeoutWidget, 1, 1)
        self.timeoutlabel = QLabel("Time has ended for these students ")
        self.timeoutList = QListWidget()
        self.timeoutlayout.addWidget(self.timeoutlabel, 0, 0)
        self.timeoutlayout.addWidget(self.timeoutList, 1, 0)

    def log(self): #Reject based on verification

        name = self.name_entry.text()
        id_number = self.id_entry.text()
        keyboard = self.keyboard_cb.isChecked()
        mouse = self.mouse_cb.isChecked()
        headset = self.headset_cb.isChecked()
        controller = self.controller_cb.isChecked()
        itemDict = {"Keyboard": keyboard, "Mouse": mouse, "Headset": headset, "Controller": controller}

        # Log the entry
        self.checkedInList.addItem(log_entry(name, id_number, itemDict))

        # Clear the text fields
        self.name_entry.clear()
        self.id_entry.clear()
        self.update_display()


    def populate(self): 
        checkedInDict = load_current_sessions()
        for id, session_info in checkedInDict.items():
            # Extract individual data from session_info
            name = session_info[0]
            id = session_info[1]
            check_in_time = session_info[2]

            # Now pass these as separate arguments
            self.checkedInList.addItem(csv_to_list_widget(name, id, check_in_time))

        

    def populateTimeout(self):
        return
        checkedInDict = load_expired_sessions("current_entries.csv")
        for key in checkedInDict:
            self.checkedInList.addItem(csv_to_list_widget(checkedInDict[key][0], checkedInDict[key][1],checkedInDict[key][2], checkedInDict[key][3]))

    def update_display(self):
        pass 

    def theme(self):
        app = QApplication(sys.argv)
        stylesheet = """
        QWidget {  
            background-color: #3e424a; /* Background color of the window */
            
        }
        QLabel {
            color: #979ca6;  /* White text color */
            font: 16px;
        }
        QPushButton {
            color: white; /* Text color */
            background-color: #02781c; /* Background color */
            font: bold 14px;
            padding: 6px;
        }
        QPushButton:pressed {
            background-color: #065718; /* Background color when pressed */
            border-style: inset;
        }
        QLineEdit {
            color: black;  /* Text color */
            background-color: #595f6b;  /* Background color */
            border: 1px solid #686e7a;  /* Border color and width */
            border-radius: 2px;  /* Rounded corners */
            padding: 2px;  /* Spacing around text */
            margin: 4px;  /* Spacing around the widget */
        }
        QCheckBox {
            spacing: 5px;
            color: #979ca6;  /* White text color */
        }
        QCheckBox::indicator {
            width: 15px;
            height: 15px;
            border: 3px solid #686e7a; /* Border color for unchecked state */
            border-radius: 5px;
            background: #595f6b; /* Background color for unchecked state */
        }

        /* Style for checked state */
        QCheckBox::indicator:checked {
            background: #3c4047; /* Background color for checked state */
        }

        /* Style for unchecked state with hover effect */
        QCheckBox::indicator:hover:!checked {
            border: 2px solid #595f6b; /* Border color on hover when unchecked */
        }

        /* Style for checked state with hover effect */
            QCheckBox::indicator:hover:checked {
            border: 2px solid #3c4047; /* Border color on hover when checked */
        }
        QListWidget::item {
            color: black;  /* Text color */
            background-color: #595f6b;  /* Background color */
        }
        QListWidget::item:selected {
            color: white; /* Text color */
            background-color: #02781c;
        }

        """
        app.setStyle('Fusion')
    
    #Runs every minute to update people that got timed out
    def routine(self):
        self.populate()