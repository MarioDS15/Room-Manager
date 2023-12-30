from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from data_handling import log_entry, update_display, remove_entry  # Make sure these are adapted for PyQt
import sys
from student import Student
import csv

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #self.theme()
        self.setWindowTitle("Room Entry Logger")

        # Create and set grid layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QGridLayout(central_widget)

        #central_widget.setStyleSheet("background-color: #696969;")  # Replace with your desired color

        #image = QLabel(self)
        #pixmap = QPixmap('logo.png')
        #pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
        #image.setPixmap(pixmap)
        #self.main_layout.addWidget(image, 0, 0, 2, 2)

        # Data entry nested grid layout
        self.dataWidget = QWidget()
        self.data_layout = QGridLayout(self.dataWidget)
        self.main_layout.addWidget(self.dataWidget, 0, 0)

        self.title_label = QLabel("Room Entry Logger")
        self.title_label.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        self.data_layout.addWidget(self.title_label, 0, 0, 1, 2)

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



        # Checked in students 
        self.checkedInWidget = QWidget()
        self.checkedInlayout = QGridLayout(self.checkedInWidget)
        self.main_layout.addWidget(self.checkedInWidget, 1, 0)

        # Students logged in display
        self.checked_in_label = QLabel("Students logged in")
        self.checkedInList = QListWidget()
        self.checkedInlayout.addWidget(self.checked_in_label, 0, 0)
        self.checkedInlayout.addWidget(self.checkedInList, 1, 0, 1, 1)


        # Testing

        self.timeoutGUI()

        # Connect button signal to slot
        self.log_button.clicked.connect(self.log)

        # Populate the list widget with existing entries
        self.populate()

    def timeoutGUI(self):
        self.timeoutWidget = QWidget()
        self.timeoutlayout = QGridLayout(self.timeoutWidget)
        self.main_layout.addWidget(self.timeoutWidget, 1, 1)
        self.timeoutlabel = QLabel("Time has ended for these students ")
        self.timeoutdisplay = QTextEdit()
        self.timeoutlayout.addWidget(self.timeoutlabel, 0, 0)
        self.timeoutlayout.addWidget(self.timeoutdisplay, 1, 0)

    def log(self):
        name = self.name_entry.text()
        id_number = self.id_entry.text()
        keyboard = self.keyboard_cb.isChecked()
        mouse = self.mouse_cb.isChecked()
        headset = self.headset_cb.isChecked()
        controller = self.controller_cb.isChecked()
        itemDict = {"Keyboard": keyboard, "Mouse": mouse, "Headset": headset, "Controller": controller}
        log_entry(name, id_number, itemDict)
        newStudent = Student(name, id_number, itemDict, True)
        self.checkedInList.addItem(newStudent.to_list_widget_item())

        self.name_entry.clear()
        self.update_display()

    def populate(self):
        with open("current_entries.csv", newline='', encoding='utf-8') as file:
            for line in file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    newStudent = Student(row[0], row[1], row[2], row[3])
                    self.checkedInList.addItem(newStudent.to_list_widget_item())

    def update_display(self):
        pass 

    def theme(self):
        app = QApplication(sys.argv)
        app.setStyle('Fusion')