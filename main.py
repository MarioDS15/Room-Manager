import subprocess
import sys
from stylesheet import stylesheet

#border: 1px solid red;


def install_packages(package_list):
    """Install Python packages using pip with error handling and pip self-upgrade."""
    # First, try upgrading pip to the latest version
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    except subprocess.CalledProcessError:
        print("Could not upgrade pip. Continuing with current version.")

    # Now, attempt to install each package
    for package in package_list:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"Failed to install package: {package}")


if __name__ == "__main__":

    required_packages = [
        'PyQt5',
        'requests',
        'pandas',
        'gspread', 
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'oauth2client', # Add any other package names here
    ]

    install_packages(required_packages)
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


    main_window = Application()
    
    # Show the main window
    main_window.show()
    
    # Start the event loop
    sys.exit(app.exec_())

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

In progress:
Application
    -Add option to only require ID

To-do:
Check if first run
User entry to edit limit per sessions [DONE]
Edit a students entry [Item, ID, Name]
Add FAQ
Try installing on mac, check for size changes
Separate sheets by weeks
Convert to application
Check out all button -> undo check out might 
Connect to google sheet (https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
"""

