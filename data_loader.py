import csv
import ast

USER_SETTINGS = "csvFiles/user_settings.csv"
ROOM_FILE = "csvFiles/room_variables.csv"
CURRENT_STUDENTS_FILE = 'csvFiles/current_entries.csv'
LOG_FILE = 'csvFiles/log_entries.csv'
ITEMS_FILE = 'csvFiles/inventory_in_use.csv'

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

def update_row(csv_file_path, key, new_value):
    with open(csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = list(csvreader)

    for row in rows:
        if row and row[0].strip() == key:  
            row[1] = str(new_value)  

    with open(csv_file_path, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

def items_to_dict(csv_file_path, id):
    with open(csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  
        for row in csvreader:
            if row and row[1].strip() == id:  
                dictionary_str = row[3].strip()
                dictionary = ast.literal_eval(dictionary_str)
                return dictionary
    return None

def csv_to_dict(csv_file_path = ROOM_FILE):
    settings_dict = {}
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) 
        for row in csvreader:
            key = row[0]
            value = row[1]
            settings_dict[key] = int(value)  
    return settings_dict



def get_student_name(id):
    with open(CURRENT_STUDENTS_FILE, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  
        print(id)
        for row in csvreader:
            if row and row[1].strip() == id: 
                return row[0].strip()
    return None