from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QListWidget, QListWidgetItem, QMessageBox, QComboBox
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

    def search_logs(self, text):
        # Clear the QListWidget before displaying new results
        self.logs.clear()

        # Open the CSV file and search
        with open(LOG_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check based on selected criteria and if the search text is in the column
                criteria = self.search_criteria.currentText().replace(' ', '_')
                if text.lower() in row[criteria].lower():
                    # Add the row description to the QListWidget
                    item_text = f"{row['Name']}, {row['ID']}, {row['Check-in time']}"
                    self.logs.addItem(item_text)

    