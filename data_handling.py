from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QListWidget, QListWidgetItem
import csv
from datetime import datetime, timedelta
from room_variables import * 
from user_settings import *
from data_loader import *
from StudentWidget import *
import csv
CSV_FILE_PATH = CURRENT_STUDENTS_FILE



def id_exists_in_file(id, file_path = CURRENT_STUDENTS_FILE):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[1] == id:  # Assuming 'id' is in the second column
                return True
    return False

def log_entry(name, id, itemDict):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if the ID already exists in current_entries.csv
    if id_exists_in_file(id, CURRENT_STUDENTS_FILE):
        print(f"ID {id} already exists in current_entries.csv")
        raise ValueError(f"ID {id} already exists in current_entries.csv")
        

    # If the ID is unique, write to both files
    for file_path in [LOG_FILE, CURRENT_STUDENTS_FILE]:
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, id, timestamp, itemDict])
    
    return csv_to_list_widget(name, id, timestamp)

def log_checkout(id):
    updated_entries = []
    current_time = datetime.now()

    with open(LOG_FILE, newline='', encoding='utf-8') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            # Assuming the ID is in the 2nd column (index 1)
            if row and row[1] == id:
                row.append(current_time.strftime('%Y-%m-%d %H:%M:%S'))  # Add current time to the row
            updated_entries.append(row)

    # Write the updated data back to the CSV file
    with open(LOG_FILE, 'w', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerows(updated_entries)

def load_current_sessions(csv_file_path):
    current_sessions = {}
    now = datetime.now()

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # Skip the header row

        for row in csvreader:
            if len(row) < 3:  # Check if the row has at least 3 elements
                continue

            id, check_in_time_str = row[1], row[2]
            check_in_time = datetime.strptime(check_in_time_str, '%Y-%m-%d %H:%M:%S')

            # Check if the session time has not exceeded 2 hours
            if now - check_in_time < session_time_limit:  # Session is still active
                current_sessions[id] = row  # Store the entire row

    return current_sessions

def load_expired_sessions(csv_file_path):
    expired_sessions = {}
    now = datetime.now()
    #session_time_limit = timedelta(hours=2)  # Define the session time limit

    with open(csv_file_path, newline='', encoding='utf-8') as file:
        csvreader = csv.reader(file)
        next(csvreader, None)  # Skip the header row
        
        for row in csvreader:
            if len(row) < 3:  # Ensure each row has at least 3 elements
                continue

            id, check_in_time_str = row[1], row[2]
            check_in_time = datetime.strptime(check_in_time_str, '%Y-%m-%d %H:%M:%S')
            
            if now - check_in_time >= session_time_limit:  # Session has expired
                expired_sessions[id] = row  # Store the entire row

    return expired_sessions

def csv_to_list_widget(name, id, check_in_time_str):
    # Format the display text for the QListWidgetItem
    check_in_time_str = check_in_time_str[10:]
    if get_time_format() == False:
        check_in_time_str = convert_to_12hr(check_in_time_str)
    display_text = f"[{check_in_time_str}] {name} (ID: {id})"
    #display_text = f"{name} (ID: {id})"
    # Create and return the QListWidgetItem
    item = StudentWidget(display_text)
    return item

def convert_to_12hr(time_string):
    time_string = time_string.split(':')
    hour = int(time_string[0])
    if hour > 12:
        hour -= 12
        time_string[0] = str(hour)
        time_string = ':'.join(time_string)
        time_string += " PM"
    elif hour == 12:
        time_string = ':'.join(time_string)
        time_string += " PM"
    elif hour == 0:
        time_string = "12:" + time_string[1] + " AM"
    else:
        time_string = ':'.join(time_string)
        time_string += " AM"
    return time_string

def check_if_session_active(id, current_sessions = CSV_FILE_PATH):
    now = datetime.now()
    if id in current_sessions:
        session_end_time = current_sessions[id] + session_time_limit
        return now < session_end_time
    return False

current_sessions = load_current_sessions(CSV_FILE_PATH)

def check_if_logged_in(id):
    if id in current_sessions:
        return True
    else:
        return False

def try_check_in(name, id):
    if check_if_session_active(id, current_sessions):
        return False
    else:
        # Check in the user and add their entry to the CSV and current sessions
        check_in_time = datetime.now()
        current_sessions[id] = check_in_time
        with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, id, check_in_time.strftime('%Y-%m-%d %H:%M:%S')])
        True

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

def verify_id(id):
    if len(id) == 9:
        if id[0] == 'g' or id[0] == 'G':
            if id[1:].isdigit():
                return True
    elif len(id) == 8:
        if id.isdigit():
            return True
    return False

def id_convert(id):
    if len(id) == 8:
        return 'G' + id
    if len(id) == 9:
        id = id.upper()
    return id

def verify_name(name):
    if len(name) > 0 and name.isalpha():
        return True
    return False

def list_widget_to_id(list_widget):
    # Extract the ID from the QListWidgetItem
    display_text = list_widget.text()
    id = display_text.split('ID: ')[1].replace(')', '')
    return id



def remove_entry(id, csv_file_path = CSV_FILE_PATH):
    updated_entries = []

    with open(csv_file_path, newline='', encoding='utf-8') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            # Assuming the ID is in the 2nd column (index 1)
            if row and row[1] == id:
                continue  # Skip this row
            updated_entries.append(row)

    # Write the updated data back to the CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerows(updated_entries)

def edit_inventory(itemDict, returning = False):
    #set_PC_count(get_PC_in_use() - 1)
    if returning:
        if itemDict["Keyboard"] and get_keyboard_in_use() < get_max_keyboard_count():
            set_keyboard_in_use(get_keyboard_in_use() - 1)
        if itemDict['Mouse'] and get_mouse_in_use() < get_max_mouse_count():
            set_mouse_in_use(get_mouse_in_use() - 1)
        if itemDict['Headset'] and get_headset_in_use() < get_max_headset_count():
            set_headset_in_use(get_headset_in_use() - 1)
        if itemDict['Controller'] and get_controller_in_use() < get_max_controller_count():
            set_controller_in_use(get_controller_in_use() - 1)
        if itemDict['Mousepad'] and get_mousepad_in_use() < get_max_mousepad_count():
            set_mousepad_in_use(get_mousepad_in_use() - 1)
        set_PC_in_use(get_PC_in_use() - 1)
    else:
        if itemDict["Keyboard"]:
            set_keyboard_in_use(get_keyboard_in_use() + 1)
        if itemDict['Mouse']:
            set_mouse_in_use(get_mouse_in_use() + 1)
        if itemDict['Headset']:
            set_headset_in_use(get_headset_in_use() + 1)
        if itemDict['Controller']:
            set_controller_in_use(get_controller_in_use() + 1)
        if itemDict['Mousepad']:
            set_mousepad_in_use(get_mousepad_in_use() + 1)
        set_PC_in_use(get_PC_in_use() + 1)


def checkInventory():
    message = ""
    if get_headset_in_use() >= get_max_headset_count():
        message += "Headsets \n "
    if get_mouse_in_use() >= get_max_mouse_count():
        message += "Mice \n"
    if get_keyboard_in_use() >= get_max_keyboard_count():
        message += "Keyboards \n"
    if get_controller_in_use() >= get_max_controller_count():
        message += "Controllers \n"
    if get_mousepad_in_use() >= get_max_mousepad_count():
        message += "Mousepads \n"
    if get_PC_in_use() >= get_max_pc_count():
        message += "PCs \n"
    if message == "":
        return False
    return message

