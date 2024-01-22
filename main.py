import subprocess
import sys
from stylesheet import stylesheet
from data_handling import *
from data_loader import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QFont, QIcon
from gui import Application
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from csv_handling import *
from room_variables import *
from csv_handling import *
import os
"""py -m PyInstaller --clean --add-data "csvFiles;csvFiles" --add-data "logo.png;." --add-data "client.json;." --noconsole --icon=logo.ico main.py"""
#border: 1px solid red;

def on_startup(loading_screen):
    """Runs on startup"""

    # Might want to check if connected to internet
    # Import packages


    # Gets all the data from the sheets and stores them locally
    retrieve_all()

    # Loads the items that are stored in the room and their quantity
    load_items()

    # Loads the items in use and their quantity from google sheets
    load_items_in_use()

    # Update the weekly log sheet
    # update_weekly_log_sheet()

    print("Startup complete")
    pass

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(get_logo()))
        self.setFixedSize(400, 400)
        self.initUI()
        self.startLoadingAnimation()  # Start the loading animation

    def initUI(self):
        layout = QVBoxLayout()

        # Logo
        logo_label = QLabel(self)
        pixmap = QPixmap(get_logo())  # Replace with your logo path
        logo_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))  # Scale logo as needed

        # Title
        self.title = QLabel("GMU Esports Check-in System")
        self.title.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignCenter)

        # Loading Text Label
        self.label = QLabel("Retrieving data from online database. Please wait.")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        layout.addWidget(self.title, alignment=Qt.AlignCenter)
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def startLoadingAnimation(self):
        self.dot_count = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateLoadingText)
        self.timer.start(1000)  # Update every second

    def updateLoadingText(self):
        self.dot_count = (self.dot_count % 3) + 1  # Cycle through 1, 2, 3
        self.label.setText(f"Retrieving data from online database. Please wait{'.' * self.dot_count}")
    
# Thread Class for Running on_startup
class StartupThread(QThread):
    finished = pyqtSignal()

    def run(self):
        on_startup(loading_screen)
        self.finished.emit()

def main():
    print("User settings path:", get_room_path())
    print("Room file path:", get_room_path())
    room_settings_path = get_room_path()
    

if __name__ == "__main__":
    from data_handling import *
    from PyQt5.QtWidgets import QApplication
    from gui import Application
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    import os
    main()
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(stylesheet)
    if not is_connected():
        QMessageBox.information(None, "Connection Error", "No internet connection detected, please reconnect to the internet and restart the program.")
        sys.exit()

    # Initialize and show loading screen
    loading_screen = LoadingScreen()
    loading_screen.show()

    # Create and start startup thread
    startup_thread = StartupThread()

    # Initialize main window but do not show it yet
    main_window = Application()

    # Function to show the main window
    def show_main_window():
        main_window.show()
        main_window.setWindowIcon(QIcon(get_logo()))
        main_window.activateWindow()
        main_window.raise_()

    # Connect the finished signal to both close the loading screen and show the main window
    startup_thread.finished.connect(loading_screen.close)
    startup_thread.finished.connect(show_main_window)

    startup_thread.start()

    # Start the event loop
    sys.exit(app.exec_())

"""Done:
Implement remove entry [DONE]
Fix display [DONE]
Auto update time (Threading?) [DONE]
Check if ID is already there [DONE]
Check out system [DONE]
Time entry option (Military v not) [DONE]
Right click [DONE]
Data validation (Prevents invalid usernames/id) [DONE]
Check if student already checked in [DONE]
Add checkout everyone button 
Add warning if items are out
Verification of id removes name
Fix clear checkboxes after submitting
Fix hovering over checkboxes [DONE]
Add check out time to log entries 
Limit sessions per day
Only one list widget should have a highlighted person
Log view window
Edit items
Handle if not connected to internet
Can't checkout individual that is timed out
User entry to edit limit per sessions [DONE]
Edit a students entry [Item, ID, Name]
Separate sheets by weeks
Loading screen while app is booting up
Items do not update on the cloud besides pc
Mousepad not updating
Handle race conditions
Add threading to reset count
Fix how room stats looks[Done?]
In progress:
Convert to application
Synch to cloud
Add logo for app
Other windows do not close when main is closed

To-do:
Import stuff


Application
    -Add option to only require ID
Check-out time not being included for logs, might have to redo find row implementation
Try installing on mac, check for size changes
Am I even downloading the weekly log?
Searching logs fucks it up [  File "log_gui.py", line 52, in search_logs
KeyError: 'ID']
Do I have to have race conditions for every function that edits logs directly
Header got deleted again
If there is no secondary window and the app is closed, theres a bug
Item and room settings not updating
"""

