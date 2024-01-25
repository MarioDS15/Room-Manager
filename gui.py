from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QListWidget, QListWidgetItem, QMessageBox, QToolBar, QMenu, QAction
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from room_settings_GUI import *
from data_handling import *
from datetime import datetime, timedelta
from StudentWidget import *
from data_loader import *
from room_stats_gui import *
from log_gui import *
from item_edit_gui import *
from FAQWindow import *
import csv
import sys
#from csv_handling import *
#from csv_handling import *
import threading
from lock import *

""" py -m PyInstaller --onefile --clean --add-data "csvFiles;csvFiles" --add-data "logo.png;." --add-data "client.json;." main.py"""
class Application(QMainWindow):
    update_gui_signal = pyqtSignal()

    #upload_file('current_entries.csv', 'csvFiles/current_entries.csv', 'text/csv')
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Office Hours Check-in System")

        self.setMinimumSize(1000, 500)
        #self.setFixedSize(900, 500)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QGridLayout(central_widget)

        self.dataWidget = QWidget()
        self.data_layout = QGridLayout(self.dataWidget)
        self.main_layout.addWidget(self.dataWidget, 1, 0)

        self.title_label = QLabel("Office Hours Check-in")
        self.title_label.setStyleSheet("color: #cfcfcf; font-size: 30px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label, 0, 0, 1, 2)
        self.toolbar()
        #self.retrieve_all()
        self.dataEntryGUI()
        self.itemEntryGUI()
        self.checkedInGUI()
        self.timeoutGUI()

        #self.aboutToQuit.connect(self.closeEvent)
        self.populate()
        self.populateTimeout()
        self.timer()
        self.otherTimer()
        
        self.update_gui_signal.connect(self.run_update_gui) 
        self.secondary_window = None
        
    def run_update_gui(self):
        """Initiates update_gui in a worker thread"""
        worker = threading.Thread(target=self.update_gui)
        worker.start()

    def update_gui(self):
        with lock:
            print("Locking from update_gui")
            retrieve_all()
            self.remove_all_list_widgets(self.checkedInList)
            self.populate()
            self.remove_all_list_widgets(self.timeoutList)
            self.populateTimeout()
            print("Unlocked from update_gui")


    #Runs every time frame to update people that got timed out
    def routine(self):
        """Runs every minute to update the display and synchs data with the cloud"""
        self.update_gui_signal.emit()

    def closeEvent(self, event):
        if self.secondary_window is not None:
            self.secondary_window.close()

    def timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.routine)
        self.timer.start(300000)
 
    def otherTimer(self):
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.routine_second)
        self.timer2.start(1000)

    def open_room_settings(self):
        """Opens the room settings window"""
        if self.secondary_window is None:  # Check if the window does not exist
            self.secondary_window = RoomSettingWindow()  # Create the window
            self.secondary_window.show()
            self.secondary_window.setAttribute(Qt.WA_DeleteOnClose)  # Ensure the window is deleted after closing
            self.secondary_window.destroyed.connect(self.on_room_settings_window_destroyed)
        else:
            self.secondary_window.show()

    def on_room_settings_window_destroyed(self):
            self.secondary_window = None  # Reset the placeholder when the window is closed

    def open_room_stats(self):
        if self.secondary_window is None:
            self.secondary_window = RoomStatsWindow()
            self.secondary_window.show()
            self.secondary_window.setAttribute(Qt.WA_DeleteOnClose)
            self.secondary_window.destroyed.connect(self.on_room_stats_window_destroyed)
        else:
            self.secondary_window.show()

    def on_room_stats_window_destroyed(self):
        self.secondary_window = None

    def open_logs(self):
        if self.secondary_window is None:
            self.secondary_window = LogsWindow()
            self.secondary_window.show()
            self.secondary_window.setAttribute(Qt.WA_DeleteOnClose)
            self.secondary_window.destroyed.connect(self.open_logs_window_destroyed)
        else:
            self.secondary_window.show()

    def open_logs_window_destroyed(self):
        self.secondary_window = None

    def open_edit_items(self, list_widget = None):
        if self.secondary_window is None:
            if list_widget.currentItem() is not None :
                id = list_widget_to_id(list_widget.currentItem())
                name = get_student_name(id)
                dict = items_to_dict(get_current_students_path(), id)
            else:
                self.throwPrompt("Edit Error", "No student selected")
                return
            self.secondary_window = EditItemsWindow(name, id, dict)
            self.secondary_window.show()
            self.secondary_window.setAttribute(Qt.WA_DeleteOnClose)
            self.secondary_window.destroyed.connect(self.open_edit_items_window_destroyed)
        else:
            self.secondary_window.show()

    def open_edit_items_window_destroyed(self):
        self.secondary_window = None

    def open_FAQ(self):
        if self.secondary_window is None:
            self.secondary_window = FAQWindow()
            self.secondary_window.show()
            self.secondary_window.setAttribute(Qt.WA_DeleteOnClose)
            self.secondary_window.destroyed.connect(self.open_FAQ_window_destroyed)
        else:
            self.secondary_window.show()

    def open_FAQ_window_destroyed(self):
        self.secondary_window = None

    def toolbar(self):
        """Creates the toolbar for the main window"""
        self.toolbar = QToolBar("Toolbar")
        toolbar = self.addToolBar("Toolbar")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)

        #self.action_button = toolbar.addAction("Application Settings")


        # Add a separator
        #toolbar.addSeparator()


        self.roomSettings = toolbar.addAction("Room Settings")
        self.roomSettings.triggered.connect(self.open_room_settings)

        self.roomStats = toolbar.addAction("Room Stats")
        self.roomStats.triggered.connect(self.open_room_stats)
    
        self.logs = toolbar.addAction("Logs")
        self.logs.triggered.connect(self.open_logs)

        self.FAQ = toolbar.addAction("FAQ")
        self.FAQ.triggered.connect(self.open_FAQ)

    def dataEntryGUI(self):
        # Name entry widgets
        self.name_label = QLabel("Enter Name")
        self.name_entry = QLineEdit()
        self.data_layout.addWidget(self.name_label, 1, 0)
        self.data_layout.addWidget(self.name_entry, 1, 1)

        # ID entry widgets
        self.id_label = QLabel("Enter ID")
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
        self.main_layout.addWidget(self.itemWidget, 1, 1)

        # Items being checked out
        self.item_label = QLabel("Items being checked out")
        self.keyboard_cb = QCheckBox("Keyboard")
        self.mouse_cb = QCheckBox("Mouse")
        self.headset_cb = QCheckBox("Headset")
        self.controller_cb = QCheckBox("Controller")
        self.mousepad_cb = QCheckBox("Mousepad")
        #self.item_layout.addWidget(self.item_label, 2, 0)
        self.item_layout.addWidget(self.keyboard_cb, 3, 0)
        self.item_layout.addWidget(self.mouse_cb, 4, 0)
        self.item_layout.addWidget(self.headset_cb, 5, 0)
        self.item_layout.addWidget(self.controller_cb, 3, 1)
        self.item_layout.addWidget(self.mousepad_cb, 4, 1)

    def checkedInGUI(self):
        """Creates the GUI for the checked in students"""
        # Checked in students 
        self.checkedInWidget = QWidget()
        self.checkedInlayout = QGridLayout(self.checkedInWidget)
        self.main_layout.addWidget(self.checkedInWidget, 2, 0)

        # Students logged in display
        self.checked_in_label = QLabel("Students logged in")
        self.checkedInList = QListWidget()
        self.checkedInList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.checkedInList.customContextMenuRequested.connect(
            lambda pos: self.show_context_menu(pos, self.checkedInList))
        self.checkedInlayout.addWidget(self.checked_in_label, 0, 0)
        self.checkedInlayout.addWidget(self.checkedInList, 1, 0, 1, 2)

        # Checkout button
        self.checkout_button = QPushButton("Checkout student")
        self.checkedInlayout.addWidget(self.checkout_button, 2, 0)  
        self.checkout_button.clicked.connect(lambda: self.checkOut(self.checkedInList))

        # Item buttons
        self.item_button = QPushButton("Check student items")
        self.checkedInlayout.addWidget(self.item_button, 2, 1)  
        self.item_button.clicked.connect(lambda: self.returnItems(self.checkedInList))

        self.undo_button = QPushButton("Undo Checkout")
        #self.checkedInlayout.addWidget(self.undo_button, 2, 2)  # Spanning 2 columns
        self.undo_button.clicked.connect(self.undo_checkout)

        self.checkedInList.itemSelectionChanged.connect(lambda: self.clear_selection(self.checkedInList))

    def timeoutGUI(self):
        """Creates the GUI for the timed out students"""
        self.timeoutWidget = QWidget()
        self.timeoutlayout = QGridLayout(self.timeoutWidget)
        self.main_layout.addWidget(self.timeoutWidget, 2, 1)
        self.timeoutlabel = QLabel("Time has ended for these students ")
        self.timeoutList = QListWidget()
        self.timeoutList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.timeoutList.customContextMenuRequested.connect(
            lambda pos: self.show_context_menu(pos, self.timeoutList))
        self.timeoutlayout.addWidget(self.timeoutlabel, 0, 0)
        self.timeoutlayout.addWidget(self.timeoutList, 1, 0, 1, 2)

        # Checkout button
        self.checkout_all_button = QPushButton("Checkout expired students")
        #self.checkout_all_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.timeoutlayout.addWidget(self.checkout_all_button, 2, 0)  
        self.checkout_all_button.clicked.connect(lambda: self.checkout_all(self.timeoutList))

        # Item buttons
        self.extra_button = QPushButton("Checkout all students")
        self.extra_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.timeoutlayout.addWidget(self.extra_button, 2, 1)  
        self.extra_button.clicked.connect(lambda: self.checkout_all(self.checkedInList))

        self.timeoutList.itemSelectionChanged.connect(lambda: self.clear_selection(self.timeoutList))

        self.timeoutlayout.setColumnStretch(0, 1)
        self.timeoutlayout.setColumnStretch(1, 1)

    def checkout_buttons_gui(self):
        """Creates the GUI for the checkout buttons"""
        self.checkout_button = QPushButton("Checkout student")
        self.data_layout.addWidget(self.log_button, 3, 0, 2, 2)  # Spanning 2 columns
        self.log_button.clicked.connect(self.log)

    def log(self): #Reject based on verification
        
        with lock:
            print("Locking from log")
            """Logs the student into the system if the information is valid, the student is not already logged in, and the student has not exceeded the amount of sessions allowed per day"""
            if verify_id(self.id_entry.text()) == False:
                self.throwPrompt("Entry Error", "Invalid ID number entered")
                return
            if verify_name(self.name_entry.text()) == False:
                self.throwPrompt("Entry Error", "Invalid name entered")
                return
            
            # Obtain information from the data entry fields
            name = self.name_entry.text()
            id_number = id_convert(self.id_entry.text())
            keyboard = self.keyboard_cb.isChecked()
            mouse = self.mouse_cb.isChecked()
            headset = self.headset_cb.isChecked()
            controller = self.controller_cb.isChecked()
            mousepad = self.mousepad_cb.isChecked()
            itemDict = {"Keyboard": keyboard, "Mouse": mouse, "Headset": headset, "Controller": controller, "Mousepad": mousepad}
            if check_if_remaining_session(id_number) == False:
                self.throwPrompt("Entry Error", "Student already exceeded amount of daily sessions allowed.")
                return
            try:
                self.checkedInList.addItem(log_entry(name, id_number, itemDict))
            except:
                self.throwPrompt("Entry Error", f"Entry with ID {id_number} already exists.")
                self.clear()
                return
            #self.set_get_prev_info(datetime.now().strftime("%H:%M:%S"), name, id_number)
            # Check if any items are out of stock
            if(checkInventory() != False):
                msg = "The following items requested are out of stock: " + checkInventory() + "\n" + "The student has still been checked in but the items might be out of stock, check room stats to monitor the items in use or check if any student forgot to check out."
                self.throwPrompt("Inventory Warning", msg)
            edit_inventory(itemDict, False)
            #self.remove_selected_item(self.checkedInList)
            self.clear()
            #upload_csv_to_sheet(CURRENT_STUDENTS_FILE, "Sheet1")
            self.upload_logs()
            print("Unlocked from log")


    def undo_checkout(self):
        self.checkedInList.addItem(get_prev_info())
        self.routine()

    def clear_selection(self, selected_list_widget):
        if selected_list_widget.currentItem() is None:
            return
        currentSelected = selected_list_widget.currentItem()
        if selected_list_widget != self.checkedInList:
            self.checkedInList.clearSelection()
            #self.timeoutList.setCurrentItem(currentSelected)
        if selected_list_widget != self.timeoutList:
            self.timeoutList.clearSelection()
            #self.checkedInList.setCurrentItem(currentSelected)

    def checkOut(self, list_widget = None, selected_student = None, all = False):
        with lock:
            """Checks out the currently selected student"""
            print("Locking from checkout")
            if selected_student is None:
                selected_student = list_widget.currentItem()
            if selected_student is None:
                selected_student = self.timeoutList.currentItem()
                list_widget = self.timeoutList
            if selected_student is None:
                self.throwPrompt("Checkout Error", "No student selected")

                return
            name = get_student_name(selected_student)
            id = list_widget_to_id(selected_student)
            dict = items_to_dict(get_current_students_path(), id)
            edit_inventory(dict, True) # Edit the inventory to reflect the checkout
            log_checkout(id) # Log the checkout in the log file
            remove_entry(id) # Remove the entry from the current entries file
            self.remove_selected_item(list_widget) # Remove the entry from the display
            if not all:
                self.upload_logs()
            print("Unlocked from checkout")

        
    def upload_logs(self):
        """Starts a thread to upload the logs to the google sheet"""
        thread = threading.Thread(target=update_sheets)
        thread.start()


    def show_context_menu(self, position, list_widget):
        item = list_widget.itemAt(position)
        if isinstance(item, StudentWidget):
            context_menu, action1, action2, action3 = item.createContextMenu()
            selected_action = context_menu.exec_(list_widget.viewport().mapToGlobal(position))

            if selected_action == action1: # Checkout
                list_widget.setCurrentItem(item)
                self.checkOut(list_widget)
            
            elif selected_action == action2: # Check items borrowed
                list_widget.setCurrentItem(item)
                self.returnItems(list_widget)
            
            elif selected_action == action3:
                list_widget.setCurrentItem(item)
                self.open_edit_items(list_widget)

    def clear(self):
        """Clears the data entry fields"""
        self.name_entry.clear()
        self.id_entry.clear()
        self.keyboard_cb.setChecked(False)
        self.mouse_cb.setChecked(False)
        self.headset_cb.setChecked(False)
        self.controller_cb.setChecked(False)
        self.mousepad_cb.setChecked(False)

    def populate(self): 
        """Populates the checked in list with the current students"""
        checkedInDict = load_current_sessions(get_current_students_path())
        for id, session_info in checkedInDict.items():
            # Extract individual data from session_info
            name = session_info[0]
            id = session_info[1]
            check_in_time = session_info[2]

            # Now pass these as separate arguments
            self.checkedInList.addItem(csv_to_list_widget(name, id, check_in_time))  

    def populateTimeout(self):
        """Populates the timeout list with the expired students"""
        checkedInDict = load_expired_sessions(get_current_students_path())
        for id, session_info in checkedInDict.items():
            name = session_info[0]
            id = session_info[1]
            check_in_time = session_info[2]
            self.timeoutList.addItem(csv_to_list_widget(name, id, check_in_time))

    def remove_selected_item(self,list_widget):
        """Removes the selected item from the list widget
        
        Args:
            list_widget (QListWidget): The list widget to remove the item from
        """

        selected_item = list_widget.currentItem()

        if selected_item:  # Check if there is a selected item
            # Get the row of the selected item
            row = list_widget.row(selected_item)
            # Remove the item at the specified row
            list_widget.takeItem(row)

    def returnItems(self, list_widget = None):
        """Throws a prompt showing the items the selected student has checked out"""
        selected_student = list_widget.currentItem()
        # Check if there is a selected item
        if selected_student is None:
            self.throwPrompt("Checkout Error", "No student selected")
            return
        
        # Obtain the information from the selected item
        id = list_widget_to_id(selected_student)
        name = get_student_name(id)
        items = items_to_dict(get_current_students_path(), id)
        message = f"{name} has checked out the following: \n"
        anyItems = False
        
        # Prepare the message to display showing which items have been checked out
        for item in items:
            if items[item] == True:
                anyItems = True
                message += f"{item}\n"
        if anyItems == False:
            message = f"{name} has not checked out any items"
        self.throwPrompt("Items Checked Out", message)

    def remove_list_widget(self, list_widget):
        """Removes the selected list widget"""
        list_widget.takeItem(list_widget.row(list_widget))
    
    def remove_all_list_widgets(self, list_widget):
        """Removes all the list widgets from the list widget
        
        Args:
            list_widget (QListWidget): The list widget to remove the items from"""
        list_widget.clear()



    def routine_second(self):
        """Runs every second to check if the user is connected to the internet"""
        if not is_connected():
            QMessageBox.information(self, "Connection Error", "No internet connection detected, please reconnect to the internet and restart the program.")
            self.close()
            return

    def checkout_all(self, list_widget):
        """Checks out all the students in the specified list widget

        Args:
            list_widget (QListWidget): The list widget to check out all the students from
        """
        for i in range(list_widget.count()):
            print(i)
            self.checkOut(list_widget, list_widget.item(i), True)
        self.remove_all_list_widgets(list_widget)
        if(list_widget == self.checkedInList): # If checking out current students, expired students need to be updated
            reset_count()
            self.checkout_all(self.timeoutList)
        self.upload_logs()

    def throwPrompt(self, title, message):
        """Throws a prompt with the specified title and message

        Args:
            title (str): The title of the prompt
            message (str): The message of the prompt
        """
        QMessageBox.information(self, title, message)