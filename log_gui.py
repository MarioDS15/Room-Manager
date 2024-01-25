from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMenu, QCheckBox, QListWidget, QListWidgetItem, QMessageBox, QComboBox, QAction
from PyQt5.QtCore import Qt
from room_variables import *

class LogsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Room Logs')
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QGridLayout(central_widget)

        self.setFixedSize(400, 300)
        self.dataWidget = QWidget()
        self.item_layout = QGridLayout(self.dataWidget)
        self.main_layout.addWidget(self.dataWidget, 1, 0)

        self.title_label = QLabel("Room Logs")
        self.main_layout.addWidget(self.title_label, 0, 0, 1, 2, Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")

        self.search_bar = QLineEdit()
        self.search_criteria = QComboBox()
        self.search_criteria.addItems(["Name", "ID"])

        self.main_layout.addWidget(self.search_bar, 1, 0)
        self.main_layout.addWidget(self.search_criteria, 1, 1)


        self.search_bar.textChanged.connect(self.search_logs)
        self.logs = QListWidget()
        self.main_layout.addWidget(self.logs, 3, 0, 1, 3)

        self.logs.setContextMenuPolicy(Qt.CustomContextMenu)
        self.logs.customContextMenuRequested.connect(self.show_context_menu)
        #self.setCentralWidget(self.logs)


    def search_logs(self, text):
        """Searches the CSV file for the given text
        Args:
            text (str): The text to search for"""
        self.logs.clear()

        # Open the CSV file and search
        with open(get_log_path(), newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check based on selected criteria and if the search text is in the column
                criteria = self.search_criteria.currentText().replace(' ', '_')
                if text.lower() in row[criteria].lower():
                    # Add the row description to the QListWidget
                    item_text = f"{row['Name']}, {row['ID']}, {row['Check-in time']}"
                    self.logs.addItem(item_text)

    def show_context_menu(self, position):
        """Shows the context menu for the QListWidget"""
        context_menu = QMenu(self.logs)
        check_items_action = QAction("Check items", self.logs)
        context_menu.addAction(check_items_action)
        check_items_action.triggered.connect(self.check_items)
        context_menu.exec_(self.logs.mapToGlobal(position))

    def check_items(self, id):
        """Checks the items a student has checked out"""
        selected_item = self.logs.currentItem()
        if selected_item:
            display_text = selected_item.text()
            id = display_text.split(',')[1].strip()
            items = items_to_dict(get_log_path(), id)
            name = get_student_name(id)
            message = "Student has checked out:\n"
            anyItems = False
            for item in items:
                if items[item] == True:
                    anyItems = True
                    message += f"{item}\n"
            if anyItems == False:
                message = f"{name} has not checked out any items"
            self.throw_message(message)

    def throw_message(self, message):
        error = QMessageBox()
        error.setWindowTitle("Error")
        error.setText(message)
        #error.setIcon(QMessageBox.Critical)
        error.exec_()