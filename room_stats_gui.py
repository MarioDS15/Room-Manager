from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QListWidget, QListWidgetItem, QMessageBox, QToolBar
from PyQt5.QtCore import Qt
from room_variables import *

class RoomStatsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Room stats Window')
        #self.setMinimumSize(400, 700)
        # Create and set grid layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QGridLayout(central_widget)

        # Data entry nested grid layout
        self.dataWidget = QWidget()
        self.item_layout = QGridLayout(self.dataWidget)
        self.main_layout.addWidget(self.dataWidget, 1, 0)

        self.title_label = QLabel("Room stats")
        self.main_layout.addWidget(self.title_label, 0, 0, 1, 2, Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        self.dataEntryGUI()


    def dataEntryGUI(self):
        self.pc_count = QLabel("{} PCs are available".format( get_max_pc_count() - get_PC_in_use()))
        self.pc_taken = QLabel("{} PCs are in use".format(get_PC_in_use()))
        self.pc_taken.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.pc_count, 0, 0)
        self.item_layout.addWidget(self.pc_taken, 0, 1)
        self.pc_count.setAlignment(Qt.AlignCenter)
        self.pc_taken.setAlignment(Qt.AlignCenter)

        self.headset_count = QLabel("{} Headsets are available".format( get_max_headset_count() - get_headset_in_use()))
        self.headset_taken = QLabel("{} Headsets are in use".format(get_headset_in_use()))
        self.headset_taken.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.headset_count, 1, 0)
        self.item_layout.addWidget(self.headset_taken, 1, 1)
        self.headset_count.setAlignment(Qt.AlignCenter)
        self.headset_taken.setAlignment(Qt.AlignCenter)

        self.mouse_count = QLabel("{} Mouses are available".format( get_max_mouse_count() - get_mouse_in_use()))
        self.mouse_taken = QLabel("{} Mouses are in use".format(get_mouse_in_use()))
        self.mouse_taken.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.mouse_count, 2, 0)
        self.item_layout.addWidget(self.mouse_taken, 2, 1)
        self.mouse_count.setAlignment(Qt.AlignCenter)
        self.mouse_taken.setAlignment(Qt.AlignCenter)
        
        self.keyboard_count = QLabel("{} Keyboards are available".format( get_max_keyboard_count() - get_keyboard_in_use()))
        self.keyboard_taken = QLabel("{} Keyboards are in use".format(get_keyboard_in_use()))
        self.keyboard_taken.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.keyboard_count, 3, 0)
        self.item_layout.addWidget(self.keyboard_taken, 3, 1)
        self.keyboard_count.setAlignment(Qt.AlignCenter)
        self.keyboard_taken.setAlignment(Qt.AlignCenter)

        self.controller_count = QLabel("{} Controllers are available".format( get_max_controller_count() - get_controller_in_use()))
        self.controller_taken = QLabel("{} Controllers are in use".format(get_controller_in_use()))
        self.controller_taken.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.controller_count, 4, 0)
        self.item_layout.addWidget(self.controller_taken, 4, 1)
        self.controller_count.setAlignment(Qt.AlignCenter)
        self.controller_taken.setAlignment(Qt.AlignCenter)

        self.mousepad_count = QLabel("{} Mousepads are available".format( get_max_mousepad_count() - get_mousepad_in_use()))
        self.mousepad_taken = QLabel("{} Mousepads are in use".format(get_mousepad_in_use()))
        self.mousepad_taken.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.mousepad_count, 5, 0)
        self.item_layout.addWidget(self.mousepad_taken, 5, 1)
        self.mousepad_count.setAlignment(Qt.AlignCenter)
        self.mousepad_taken.setAlignment(Qt.AlignCenter)


        self.warning_label = QLabel("\nIf there are any items that are currently in the negatives:\n Check inventory and update the counts in the room settings tab.\nCheck if someone was not checked out.\nCheck if a student requested the wrong items.\n\nAll items should be in the positives after everyone is checked out.")
        self.warning_label.setStyleSheet('color: #747982;')
        self.warning_label.setAlignment(Qt.AlignCenter)
        self.item_layout.addWidget(self.warning_label, 6, 0, 1, 2)
        pass

    def throw_error(self, message):
        error = QMessageBox()
        error.setWindowTitle("Error")
        error.setText(message)
        error.setIcon(QMessageBox.Critical)
        error.exec_()