import csv
import ast
from datetime import date, datetime

USER_SETTINGS = "csvFiles/user_settings.csv"
ROOM_FILE = "csvFiles/room_variables.csv"
CURRENT_STUDENTS_FILE = 'csvFiles/current_entries.csv'
LOG_FILE = 'csvFiles/log_entries.csv'
ITEMS_FILE = 'csvFiles/inventory_in_use.csv'
CURRENT_WEEK = 'csvFiles/current_week.csv'



def csv_to_dict(csv_file_path):
    settings = {}
    with open(csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  
        for row in csvreader:
            if row and len(row) == 2:  
                key, value = row[0].strip(), row[1].strip()
                settings[key] = int(value) 
    return settings

def get_row_number(id, csv_file_path = LOG_FILE):
    """
    Gets the row number of a specific user that is currently checked in

    Args:
        id (str): The id of the user
        csv_file_path (str): The path to the csv file
    
    Returns:
        int: The row number of the user
    """
    with open(csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # Skip the header
        # Initialize row index counter
        row_index = 0  # Starting from 1 to account for the header row
        for row in csvreader:
            row_index += 1  # Increment row index for each row
            if row and row[1].strip() == id and len(row) < 5:
                return row_index
    return None


def items_to_dict(csv_file_path, id):
    """
    Converts the items borrowed from a specific user and turns it into a dict [ Does not work if user appears more than once]

    Args:
        csv_file_path (str): The path to the csv file
        id (str): The id of the user

    Returns:
        dict: The dictionary of items borrowed
    """
    with open(csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  
        for row in csvreader:
            if row and row[1].strip() == id:  
                dictionary_str = row[3].strip()
                dictionary = ast.literal_eval(dictionary_str)
                return dictionary
    return None

def update_dict(id, dict):
    """
    Updates the items borrowed from a specific user

    Args:
        csv_file_path (str): The path to the csv file
        id (str): The id of the user
        dict (dict): The dictionary of items borrowed

    Returns:
        dict: The dictionary of items borrowed
    """
    file_path = LOG_FILE
    with open(file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = list(csvreader)
    rowNumber = 0
    for row in rows:
        if rowNumber == get_row_number(id): 
            row[3] = str(dict)  
        rowNumber += 1

    with open(file_path, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)
    
    csv_file_path = CURRENT_STUDENTS_FILE
    with open(csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = list(csvreader)

    for row in rows:
        if row and row[1].strip() == id:  
            row[3] = str(dict)  

    with open(csv_file_path, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)


def csv_to_dict(csv_file_path = ROOM_FILE):
    """
    Used for inventory csvs, converts the csv to a dictionary.

    Args:
        csv_file_path (str): The path to the csv file

    Returns:
        dict: The dictionary of items borrowed
    """
    settings_dict = {}
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) 
        for row in csvreader:
            key = row[0]
            value = row[1]
            settings_dict[key] = int(value)  
    return settings_dict


def update_row(csv_file_path, key, new_value):
    """
    Updates a specific row in an inventory csv.

    Args:
        csv_file_path (str): The path to the csv file
        key (str): The key of the row to update
        new_value (str): The new value of the row
    """
    with open(csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = list(csvreader)

    for row in rows:
        if row and row[0].strip() == key:  
            row[1] = str(new_value)  

    with open(csv_file_path, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)


def get_student_time(id):
    """
    Gets the time a specific user checked in.

    Args:
        id (str): The id of the user

    Returns:
        str: The time the user checked in
    """
    with open(LOG_FILE, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  
        for row in csvreader:
            if row and row[1].strip() == id:  
                return (row[2][-8:])
    return None

def get_student_name(id):
    """
    Gets the name of a specific user.

    Args:
        id (str): The id of the user

    Returns:
        str: The name of the user
    """
    with open(CURRENT_STUDENTS_FILE, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  
        #print(id)
        for row in csvreader:
            if row and row[1].strip() == id: 
                return row[0].strip()
    return None

def find_entries_from_today(csv_file_path = LOG_FILE):
    """
    Finds all entries from today.

    Args:
        csv_file_path (str): The path to the csv file

    Returns:
        list: A list of all entries from today
    """
    today = datetime.now().date()  # Get the current date as a date object
    today_entries = []  # List to store today's entries

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Parse the 'Check-in time' to a datetime object and get the date part
            check_in_date = datetime.strptime(row['Check-in time'], '%Y-%m-%d %H:%M:%S').date()
            if check_in_date == today:
                today_entries.append(row)  # If the dates match, add to the list
    #print("Todays entries:" + str(today_entries))
    return today_entries

