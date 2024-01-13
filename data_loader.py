import csv
import ast

USER_SETTINGS = "user_settings.csv"
ROOM_FILE = "room_variables.csv"
CURRENT_STUDENTS_FILE = 'current_entries.csv'
LOG_FILE = 'log_entries.csv'
ITEMS_FILE = 'inventory_in_use.csv'

def csv_to_dict(csv_file_path):
    settings = {}
    with open(csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # Skip the header row
        for row in csvreader:
            if row and len(row) == 2:  # Ensure the row has exactly two columns
                key, value = row[0].strip(), row[1].strip()
                settings[key] = int(value)  # Convert value to int since they appear to be numeric
    return settings

def update_row(csv_file_path, key, new_value):
    # Read the CSV file into a list of lists
    with open(csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = list(csvreader)

    # Update the value in the list of lists
    for row in rows:
        if row and row[0].strip() == key:  # Ensure the row has at least one column
            row[1] = str(new_value)  # Convert value to string since they appear to be numeric

    # Write the updated list of lists back to the CSV file
    with open(csv_file_path, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

def items_to_dict(csv_file_path, id):
    with open(csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # Skip the header row
        for row in csvreader:
            if row and row[1].strip() == id:  # Ensure the row has at least one column
                dictionary_str = row[3].strip()
                dictionary = ast.literal_eval(dictionary_str)
                return dictionary
    return None

def csv_to_dict(csv_file_path = ROOM_FILE):
    # Initialize an empty dictionary
    settings_dict = {}
    
    # Open the CSV file for reading
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        # Create a CSV reader object
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row
        
        # Iterate over the rows in the CSV
        for row in csvreader:
            # The first column is the key, and the second column is the value
            key = row[0]
            value = row[1]
            settings_dict[key] = int(value)  # Convert value to integer
    
    # Return the dictionary
    return settings_dict



def get_student_name(id):
    with open(CURRENT_STUDENTS_FILE, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # Skip the header row
        print(id)
        for row in csvreader:
            if row and row[1].strip() == id:  # Ensure the row has at least one column
                return row[0].strip()
    return None