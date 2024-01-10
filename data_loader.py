import csv

USER_SETTINGS = "user_settings.csv"
ROOM_FILE = "room_variables.csv"
CURRENT_STUDENTS_FILE = 'current_entries.csv'
LOG_FILE = 'log_entries.csv'

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