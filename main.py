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
        'requests',  # Add any other package names here
    ]

    install_packages(required_packages)
    from data_handling import *
    from PyQt5.QtWidgets import QApplication
    from gui import Application
    # Create an instance of QApplication
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(stylesheet)
    # Create an instance of your application's main window
    main_window = Application()
    
    # Show the main window
    main_window.show()
    
    # Start the event loop
    sys.exit(app.exec_())

"""
Add rented items to display [Don't need]
Implement remove entry [DONE]
Fix display (grid) [DONE]
Auto update time (Threading)
Check out system [DONE]
Make time entry be 12 hour format and do not include seconds [DONE]
Add checkout everyone button
Add tabs, FAQ, quick fix, item inventory, etc
Data validation [DONE]
Fix hovering over checkboxes [DONE]
Hard reset button [Don't need]
Scroll display [Don't need]
Right click
Check if student already checked in [DONE]
Add option to only require ID
Connect to google sheet (https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
"""

