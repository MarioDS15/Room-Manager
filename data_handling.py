from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QListWidget, QListWidgetItem
import csv
from datetime import datetime, timedelta
from room_variables import * 
from data_loader import *
from StudentWidget import *
import csv
from lock import *
CSV_FILE_PATH = get_current_students_path()


def id_exists_in_file(id, file_path = get_current_students_path()):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[1] == id:  # Assuming 'id' is in the second column
                return True
    return False

def log_entry(name, id, itemDict):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if the ID already exists in current_entries.csv
    if id_exists_in_file(id, get_current_students_path()):
        raise ValueError(f"ID {id} already exists in current_entries.csv")
        
    # If the ID is unique, write to both files
    for file_path in [get_log_path(), get_current_students_path()]:
        print("Writing to: " + file_path)
        
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, id, timestamp, itemDict])
    
    return csv_to_list_widget(name, id, timestamp)



def check_if_remaining_session(id):
    todayEntries = find_entries_from_today()
    if todayEntries:
        print(get_session_limit())
        if sum(entry['ID'] == id for entry in todayEntries) <= get_session_limit():
            print("True")
            return True
    else:
        return True
    return False

def log_checkout(id):
    updated_entries = []
    current_time = datetime.now()
    print("Editing file")
    with open(get_log_path(), newline='', encoding='utf-8') as file:
        csvreader = csv.reader(file)
        rowNumber = 0
        for row in csvreader:
            print(id, rowNumber, get_row_number(id),row)
            
            # Assuming the ID is in the 2nd column (index 1)
            if rowNumber == get_row_number(id):
                if len(row) < 5:
                    row.append(current_time.strftime('%Y-%m-%d %H:%M:%S'))  
                else:
                    row[4] = current_time.strftime('%Y-%m-%d %H:%M:%S')
            rowNumber += 1
            updated_entries.append(row)

    # Write the updated data back to the CSV file
    with open(get_log_path(), 'w', newline='', encoding='utf-8') as file:
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
    """Loads all expired sessions from the CSV file.
    
    Args:
        csv_file_path (str): The path to the CSV file
        
    Returns:    
        dict: A dictionary containing all expired sessions"""
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
    """Converts a CSV row to a QListWidgetItem.
    
    Args:
        name (str): The name of the student
        id (str): The ID of the student
        check_in_time_str (str): The time the student checked in

    Returns:
        QListWidgetItem: The converted QListWidgetItem
    """
    # Format the display text for the QListWidgetItem
    check_in_time_str = check_in_time_str[10:]
    if True: #if get_time_format() == False:
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

def check_if_session_active(id, current_sessions = get_current_students_path()):
    """Checks if the session is still active.
    
    Args:
        id (str): The ID of the student to be checked
        
    Returns:
        bool: Whether the session is active or not"""
    now = datetime.now()
    if id in current_sessions:
        session_end_time = current_sessions[id] + session_time_limit
        return now < session_end_time
    return False

current_sessions = load_current_sessions(CSV_FILE_PATH)

def check_if_logged_in(id): 
    """Checks if the student is already logged in.
    
    Args:
        id (str): The ID of the student to be checked
        
    Returns:
        bool: Whether the student is logged in or not
    """
    if id in current_sessions:
        return True
    else:
        return False

def checkTimeout(student):
    """Checks if the time limit has been exceeded for a specific student.
    
    Args:
        student (Student): The student to be checked
    """
    current_time = datetime.now()
    entry_time = datetime.strptime(student.checkintimeHour, '%H:%M')
    if current_time - entry_time > timedelta(hours=2):
        return True
    else:
        return False

def timeover():
    """Checks if the time limit has been exceeded for any of the current sessions."""
    updated_entries = []
    current_time = datetime.now()

    with open("current_entries.csv", newline='', encoding='utf-8') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            # Assuming the timestamp is in the 3rd column (index 2)
            # and in the format 'YYYY-MM-DD HH:MM:SS'
            if(row == []):
                continue
            entry_time = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')

            if checkTimeout:
                updated_entries.append(row)
    # Write the updated data back to the CSV file
    with open("current_entries.csv", 'w', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerows(updated_entries)

def verify_id(id):
    """Checks if the ID is valid (if it contains 8 digits and if only alphabetical character is a G at the start).
    
    Args:
        id (str): The ID to be verified
        
    Returns:
        bool: Whether the ID is valid or not"""
    if len(id) == 9:
        if id[0] == 'g' or id[0] == 'G':
            if id[1:].isdigit():
                return True
    elif len(id) == 8:
        if id.isdigit():
            return True
    return False

def id_convert(id):
    """Converts the ID to the correct format."""
    if len(id) == 8:
        return 'G' + id
    if len(id) == 9:
        id = id.upper()
    return id

def verify_name(name):
    """Checks if the name is valid."""
    if len(name) > 0 and name.isalpha():
        return True
    return False

def list_widget_to_id(list_widget):
    """Extracts the ID from a QListWidgetItem."""
    # Extract the ID from the QListWidgetItem
    display_text = list_widget.text()
    id = display_text.split('ID: ')[1].replace(')', '')
    return id

def remove_entry(id, csv_file_path = get_current_students_path()):
    """Removes an entry from current students

    Args:
        id (str): The ID of the student to be removed
        csv_file_path (str, optional): The path to the CSV file. Defaults to CSV_FILE_PATH."""
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
    """Edits the inventory based on the itemDict.
    
    Args:
        itemDict (dict): A dictionary containing the items to be checked in/out.
        returning (bool, optional): Whether the items are being checked in or out. Defaults to False."""
    #if not itemDict["Keyboard"]:
        #return
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
    """Checks if there are any items out of stock."""
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

prevName = ""  
prevID = ""
prevItems = {}
prevCheckInTime = ""

prevNameTimed = ""
prevIDTimed = ""
prevItemsTimed = {}
prevCheckInTimeTimed = ""

def set_prev_info(time, name, id):
    global prevName
    global prevID
    global prevCheckInTime
    prevCheckInTime = time
    prevName = name
    prevID = id

def get_prev_info():
    return f"[{prevCheckInTime}] {prevName} (ID: {prevID})"

def get_monday_date():
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    return monday

def get_entries_from_current_week():
    # Get the start date of the current week
    start_date = get_monday_date()

    # Get the start date of the next week
    next_week_start_date = start_date + timedelta(days=7)

    # Read the logs file
    entries_from_current_week = []
    try:
        with open(get_log_path(), 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Read the header row
            if not headers:
                print("The log file is empty.")
                return entries_from_current_week
            
            for entry in reader:
                if entry:  # Check if the row is not empty
                    try:
                        date_str = entry[2].strip()
                        entry_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        if start_date <= entry_date < next_week_start_date:
                            entries_from_current_week.append(entry)
                    except ValueError:
                        # Handle or log the error if the date format is incorrect
                        print(f"Invalid date format in entry: {entry[2][:10]}")

    except StopIteration:
        # Handle the case where the log file has only headers or is empty
        print("No entries in the log file.")

    write_entries_to_csv(entries_from_current_week)
    return entries_from_current_week

def write_entries_to_csv(entries, csv_file_path= get_current_week_path()):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)  # Read the first line for headers

    # Open the file in write mode and write headers and new entries
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write the headers back
        if headers:
            csvwriter.writerow(headers)

        # Write the new entries
        for entry in entries:
            csvwriter.writerow(entry)

def formatted_monday_date():
    return get_monday_date().strftime('%m/%d/%Y')

