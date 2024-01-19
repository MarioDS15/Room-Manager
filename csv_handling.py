import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
from data_loader import *
import socket
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('client.json', scopes=scope)

# Authorize the credentials with gspread
gc = gspread.authorize(creds)

def upload_csv_to_sheet(csv_file_path, sheet_name = None):
    # Define the scope of the application
    global scope
    global gc
    global sheet

    # Open the Google Sheet
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1GoRyPMKROvDTHMwj3MQRT7pRbovElxDQUoMRK7_0jUM/edit?usp=sharing").sheet1

    sheet.clear()
    # Read the CSV file data

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    # Upload CSV data to the first sheet of the Google Sheet
    sheet.update('A1', data)


def upload_logs(file):
    global scope
    global gc
    global sheet
    # Load credentials from the downloaded JSON key file
    sheetName = ""
    if file == LOG_FILE:
        sheetName = "Logs"
    elif file == CURRENT_STUDENTS_FILE:
        sheetName = "Current Entries"
    elif file == ROOM_FILE:
        sheetName = "Room Settings"
    elif file == ITEMS_FILE:
        sheetName = "Item Settings"
    # Open the Google Sheet
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1GoRyPMKROvDTHMwj3MQRT7pRbovElxDQUoMRK7_0jUM/edit?usp=sharing")


    worksheet = sheet.worksheet(sheetName)
    worksheet.clear()
    # Read the CSV file data

    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    # Upload CSV data to the first sheet of the Google Sheet
    worksheet.update('A1', data)


def update_sheets():
    upload_logs(CURRENT_STUDENTS_FILE)
    upload_logs(LOG_FILE)
    upload_logs(ROOM_FILE)
    upload_logs(ITEMS_FILE)

def retrieve_sheet(sheet_name):
    global scope
    global gc
    global sheet
    print("Retrieving" + sheet_name)
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1GoRyPMKROvDTHMwj3MQRT7pRbovElxDQUoMRK7_0jUM/edit?usp=sharing").worksheet(sheet_name)


    list_of_lists = sheet.get_all_values()
    fileName = ""

    if sheet_name == "Logs":
        fileName = LOG_FILE
    elif sheet_name == "Current Entries":
        fileName = CURRENT_STUDENTS_FILE
    elif sheet_name == "Room Settings":
        fileName = ROOM_FILE
    elif sheet_name == "Item Settings":
        fileName = ITEMS_FILE

    
    with open(fileName, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(list_of_lists)

def retrieve_all():
    retrieve_sheet("Room Settings")
    retrieve_sheet("Item Settings")
    retrieve_sheet("Current Entries")
    retrieve_sheet("Logs")

def is_connected(hostname="8.8.8.8", port=53, timeout=3):
    """
    Check if there is an internet connection.
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((hostname, port))
        return True
    except socket.error as ex:
        return False


#retrieve_all()
#retrieve_sheet("Logs")
#update_sheets()


#upload_csv_to_sheet(CURRENT_STUDENTS_FILE, "Sheet1")
