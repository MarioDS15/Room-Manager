import subprocess
import sys
from stylesheet import stylesheet
from data_handling import *
from PyQt5.QtWidgets import QApplication
from gui import Application
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from csv_handling import *
from room_variables import *
from csv_handling import *
import os

#border: 1px solid red;


def on_startup():
    #retrieve_all()
    load_items()
    load_items_in_use()

    pass

if __name__ == "__main__":

    from data_handling import *
    from PyQt5.QtWidgets import QApplication
    from gui import Application
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    import os
    # Create an instance of QApplication
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(stylesheet)

    on_startup()
    main_window = Application()
    
    # Show the main window
    main_window.show()
    
    # Start the event loop
    sys.exit(app.exec_())
    #on_startup()


"""
Done:
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

In progress:
Convert to application
Synch to cloud

To-do:
Loading screen while app is booting up
Handle race conditions
Application
    -Add option to only require ID
Add FAQ
Try installing on mac, check for size changes
"""

