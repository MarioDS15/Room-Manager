from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QListWidget, QListWidgetItem
import csv
from datetime import datetime, timedelta
from user_variables import * 
CSV_FILE_PATH = 'current_entries.csv'



def id_exists_in_file(id, file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[1] == id:  # Assuming 'id' is in the second column
                return True
    return False

def log_entry(name, id, itemDict):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if the ID already exists in current_entries.csv
    if id_exists_in_file(id, 'current_entries.csv'):
        print(f"Entry with ID {id} already exists.") # Change to prompt pop up
        return  

    # If the ID is unique, write to both files
    for file_path in ['log_entries.csv', 'current_entries.csv']:
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, id, timestamp, itemDict])
    
    return csv_to_list_widget(name, id, timestamp)
    
def load_current_sessions():
    current_sessions = {}
    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) >= 3:  # Check if the row has at least 3 elements
                id = row[1]
                current_sessions[id] = row  # Store the entire row
    return current_sessions

def load_expired_sessions(csv_file_path):
    expired_sessions = {}
    now = datetime.now()

    with open(csv_file_path, newline='', encoding='utf-8') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            id, check_in_time_str = row[1], row[2]
            check_in_time = datetime.strptime(check_in_time_str, '%Y-%m-%d %H:%M:%S')
            
            if now - check_in_time >= session_time_limit:  # Session has expired
                expired_sessions[id] = row  # Store the entire row, or specific parts as needed

    return expired_sessions

def csv_to_list_widget(name, id, check_in_time_str):
    # Format the display text for the QListWidgetItem
    display_text = f"{name} (ID: {id}) - {check_in_time_str}"
    # Create and return the QListWidgetItem
    item = QListWidgetItem(display_text)
    return item


def check_if_session_active(id, current_sessions):
    now = datetime.now()
    if id in current_sessions:
        session_end_time = current_sessions[id] + session_time_limit
        return now < session_end_time
    return False

# At application startup
current_sessions = load_current_sessions()

# When someone tries to check in
def try_check_in(name, id):
    if check_if_session_active(id, current_sessions):
        print(f"User {name} with ID {id} already has an active session.")
    else:
        # Check in the user and add their entry to the CSV and current sessions
        check_in_time = datetime.now()
        current_sessions[id] = check_in_time
        with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, id, check_in_time.strftime('%Y-%m-%d %H:%M:%S')])
        print(f"User {name} checked in successfully.")


def checkTimeout(student):
    current_time = datetime.now()
    entry_time = datetime.strptime(student.checkintimeHour, '%H:%M')
    if current_time - entry_time > timedelta(hours=2):
        return True
    else:
        return False

def timeover():
    updated_entries = []
    current_time = datetime.now()

    with open("current_entries.csv", newline='', encoding='utf-8') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            # Assuming the timestamp is in the 3rd column (index 2)
            # and in the format 'YYYY-MM-DD HH:MM:SS'
            if(row == []):
                continue
            print(row)
            entry_time = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')

            if checkTimeout:
                updated_entries.append(row)
            else:
                print("Not timed out")

    # Write the updated data back to the CSV file
    with open("current_entries.csv", 'w', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerows(updated_entries)


