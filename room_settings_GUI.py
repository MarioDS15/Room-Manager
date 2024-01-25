from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QListWidget, QListWidgetItem, QMessageBox, QToolBar
from PyQt5.QtCore import Qt
from room_variables import *
from csv_handling import *
from threading import Thread

class RoomSettingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Room settings Window')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QGridLayout(central_widget)

        self.dataWidget = QWidget()
        self.item_layout = QGridLayout(self.dataWidget)
        self.main_layout.addWidget(self.dataWidget, 1, 0)

        self.title_label = QLabel("Room Settings")
        self.main_layout.addWidget(self.title_label, 0, 0, 1, 2, Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        self.dataEntryGUI()


    def dataEntryGUI(self):
        """
        Creates the GUI for the room settings window"""
        total_hours = session_time_limit.days * 24 + session_time_limit.seconds // 3600
        self.Time_limit = QLabel("Enter room time limit")
        self.Time_limit_entry = QLineEdit()
        self.current_time_limit = QLabel(f"Current time limit: {total_hours} hrs")
        self.current_time_limit.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.Time_limit, 0, 0)
        self.item_layout.addWidget(self.Time_limit_entry, 0, 1)
        self.item_layout.addWidget(self.current_time_limit, 0, 2)

        self.PC_count = QLabel("Update PC count")
        self.PC_count_entry = QLineEdit()
        self.current_pc_count = QLabel(f"PC count: {get_max_pc_count()}")
        self.current_pc_count.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.PC_count, 1, 0)
        self.item_layout.addWidget(self.PC_count_entry, 1, 1)
        self.item_layout.addWidget(self.current_pc_count, 1, 2)

        self.Headset_count = QLabel("Update Headset count")
        self.Headset_count_entry = QLineEdit()
        self.current_headset_count = QLabel(f"Headset count: {get_max_headset_count()}")
        self.current_headset_count.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.Headset_count, 2, 0)
        self.item_layout.addWidget(self.Headset_count_entry, 2, 1)
        self.item_layout.addWidget(self.current_headset_count, 2, 2)

        self.Mouse_count = QLabel("Update Mouse count")
        self.Mouse_count_entry = QLineEdit()
        self.current_mouse_count = QLabel(f"Mouse count: {get_max_mouse_count()}")
        self.current_mouse_count.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.Mouse_count, 3, 0)
        self.item_layout.addWidget(self.Mouse_count_entry, 3, 1)
        self.item_layout.addWidget(self.current_mouse_count, 3, 2)

        self.Keyboard_count = QLabel("Update Keyboard count")
        self.Keyboard_count_entry = QLineEdit()
        self.current_keyboard_count = QLabel(f"Keyboard count: {get_max_keyboard_count()}")
        self.current_keyboard_count.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.Keyboard_count, 4, 0)
        self.item_layout.addWidget(self.Keyboard_count_entry, 4, 1)
        self.item_layout.addWidget(self.current_keyboard_count, 4, 2)

        self.Controller_count = QLabel("Update Controller count")
        self.Controller_count_entry = QLineEdit()
        self.current_controller_count = QLabel(f"Controller count: {get_max_controller_count()}")
        self.current_controller_count.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.Controller_count, 5, 0)
        self.item_layout.addWidget(self.Controller_count_entry, 5, 1)
        self.item_layout.addWidget(self.current_controller_count, 5, 2)

        self.Mousepad_count = QLabel("Update Mousepad count")
        self.Mousepad_count_entry = QLineEdit()
        self.current_mousepad_count = QLabel(f"Mousepad count: {get_max_mousepad_count()}")
        self.current_mousepad_count.setStyleSheet('color: #747982;')
        self.item_layout.addWidget(self.Mousepad_count, 6, 0)
        self.item_layout.addWidget(self.Mousepad_count_entry, 6, 1)
        self.item_layout.addWidget(self.current_mousepad_count, 6, 2)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_threaded)
        self.item_layout.addWidget(self.save_button, 7, 0, 2, 3)

        pass

    def save(self):
        """
        Saves the settings to the room settings file"""
        #Time
        if self.Time_limit_entry.text():
            time_limit = self.Time_limit_entry.text()
            if time_limit.isdigit():
                set_time_limit(int(time_limit))
                total_hours = get_session_time_limit().days * 24 + get_session_time_limit().seconds // 3600
                self.current_time_limit.setText(f"Current time limit: {total_hours} hrs")
                self.Time_limit_entry.setText("")
            else:
                self.throw_message("Please enter a valid time limit (in hours)")
                self.Time_limit_entry.setText("")
        
        #PC
        if self.PC_count_entry.text():
            pc_count = self.PC_count_entry.text()
            print(pc_count)
            if pc_count.isdigit():
                set_max_pc_count(int(pc_count))
                self.current_pc_count.setText(f"PC count: {get_max_pc_count()}")
                self.PC_count_entry.setText("")
            else:
                print("Throwing Message")
                self.throw_message("Please enter a valid PC count")
                self.PC_count_entry.setText("")
            
        #Headset
        if self.Headset_count_entry.text():
            headset_count = self.Headset_count_entry.text()
            if headset_count.isdigit():
                set_headset_count(int(headset_count))
                self.current_headset_count.setText(f"Headset count: {get_max_headset_count()}")
                self.Headset_count_entry.setText("")
            else:
                self.throw_message("Please enter a valid headset count")
                self.Headset_count_entry.setText("")

            
        #Mouse
        if self.Mouse_count_entry.text():
            mouse_count = self.Mouse_count_entry.text()
            if mouse_count.isdigit():
                set_mouse_count(int(mouse_count))
                self.current_mouse_count.setText(f"Mouse count: {get_max_mouse_count()}")
                self.Mouse_count_entry.setText("")
            else:
                self.throw_message("Please enter a valid mouse count")
                self.Mouse_count_entry.setText("")

            
        #Keyboard
        if self.Keyboard_count_entry.text():
            keyboard_count = self.Keyboard_count_entry.text()
            if keyboard_count.isdigit():
                set_keyboard_count(int(keyboard_count))
                self.current_keyboard_count.setText(f"Keyboard count: {get_max_keyboard_count()}")
                self.Keyboard_count_entry.setText("")
            else:
                self.throw_message("Please enter a valid keyboard count")
                self.Keyboard_count_entry.setText("")

        
        #Controller
        if self.Controller_count_entry.text():
            controller_count = self.Controller_count_entry.text()
            if controller_count.isdigit():
                set_controller_count(int(controller_count))
                self.current_controller_count.setText(f"Controller count: {get_max_controller_count()}")
                self.Controller_count_entry.setText("")
            else:
                self.throw_message("Please enter a valid controller count")
                self.Controller_count_entry.setText("")

        
        #Mousepad
        if self.Mousepad_count_entry.text():
            mousepad_count = self.Mousepad_count_entry.text()
            if mousepad_count.isdigit():
                set_mousepad_count(int(mousepad_count))
                self.current_mousepad_count.setText(f"Mousepad count: {get_max_mousepad_count()}")
                self.Mousepad_count_entry.setText("")
            else:
                self.throw_message("Please enter a valid mousepad count")
                self.Mousepad_count_entry.setText("")

            
        update_sheet(get_room_path())
        pass

    def save_threaded(self):
        """Runs the save function in a separate thread."""
        self.save()
        def task():
            update_sheet(get_room_path())
        
        # Create and start the thread
        thread = Thread(target=task)
        thread.start()

    def throw_message(self, message):
        QMessageBox.information(self, "Error", message)