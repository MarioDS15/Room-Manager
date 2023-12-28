import subprocess
import sys
from data_handling import log_entry, update_display, remove_entry  # Ensure these are adapted for PyQt
from gui import Application

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
        'pyqt5',
        'requests',  # Add any other package names here
    ]

    install_packages(required_packages)
    from PyQt5.QtWidgets import QApplication

    # Create an instance of QApplication
    app = QApplication(sys.argv)
    
    # Create an instance of your application's main window
    main_window = Application()
    
    # Show the main window
    main_window.show()
    
    # Start the event loop
    sys.exit(app.exec_())

"""
Add rented items to display
Implement remove entry
Fix display (grid)
Auto update time (Threading)
Check out system
Make time entry be 12 hour format and do not include seconds
Add checkout everyone button
Add tabs, FAQ, quick fix, item inventory, etc

"""