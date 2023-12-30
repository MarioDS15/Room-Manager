import subprocess
import sys
from data_handling import log_entry, update_display, remove_entry  # Ensure these are adapted for PyQt
#border: 1px solid red;
stylesheet = """
QWidget {  
    background-color: #3e424a; /* Background color of the window */
    
}
QLabel {
    color: #979ca6;  /* White text color */
    fontsize: 16px;
}
QPushButton {
    color: white; /* Text color */
    background-color: #02781c; /* Background color */
    font: bold 14px;
    padding: 6px;
}
QPushButton:pressed {
    background-color: #065718; /* Background color when pressed */
    border-style: inset;
}
QLineEdit {
    color: black;  /* Text color */
    background-color: #595f6b;  /* Background color */
    border: 1px solid #686e7a;  /* Border color and width */
    border-radius: 2px;  /* Rounded corners */
    padding: 2px;  /* Spacing around text */
    margin: 4px;  /* Spacing around the widget */
}
QCheckBox {
    spacing: 5px;
    color: #979ca6;  /* White text color */
}
QCheckBox::indicator {
    width: 15px;
    height: 15px;
    border: 3px solid #686e7a; /* Border color for unchecked state */
    border-radius: 5px;
    background: #595f6b; /* Background color for unchecked state */
}

/* Style for checked state */
QCheckBox::indicator:checked {
    background: #3c4047; /* Background color for checked state */
}

/* Style for unchecked state with hover effect */
QCheckBox::indicator:hover:!checked {
    border: 2px solid #595f6b; /* Border color on hover when unchecked */
}

/* Style for checked state with hover effect */
    QCheckBox::indicator:hover:checked {
    border: 2px solid #3c4047; /* Border color on hover when checked */
}
QListWidget::item {
    color: black;  /* Text color */
    background-color: #595f6b;  /* Background color */
}
QListWidget::item:selected {
    color: white; /* Text color */
    background-color: #02781c;
}

"""

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
Add rented items to display
Implement remove entry
Fix display (grid)
Auto update time (Threading)
Check out system
Make time entry be 12 hour format and do not include seconds
Add checkout everyone button
Add tabs, FAQ, quick fix, item inventory, etc
Data validation
Fix hovering over checkboxes
"""