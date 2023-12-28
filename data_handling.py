import csv
from datetime import datetime

def log_entry(name, id):
    # Get data from the GUI fields
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Store the data locally or upload it to Google Sheets here
    with open('log_entries.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, id, timestamp])
    
    with open('current_entries.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, id, timestamp])

def update_display():
    display_text = ""
    with open('current_entries.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            display_text += f"Name: {row[0]}, ID: {row[1]}, Timestamp: {row[2]}\n"
    return display_text

def remove_entry(name):
    entries = []

    # Read all entries from the CSV file
    with open("current_entries.csv", mode='r') as file:
        entries = list(csv.reader(file))

    # Find and remove the entries with the specified name
    updated_entries = [entry for entry in entries if entry[0] != name]

    # Write the updated entries back to the CSV file
    with open("current_entries.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_entries)

    update_display()