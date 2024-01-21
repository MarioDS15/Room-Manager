import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import os
import csv
from data_loader import *
import socket
from datetime import datetime, timedelta
from data_handling import *
from data_loader import *
import threading

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name(get_json(), scopes=scope)

# Authorize the credentials with gspread
gc = gspread.authorize(creds)

sheet_lock = threading.Lock()
headers = ['Name', 'ID', 'Check-in time', 'Equipment', 'Check-out Time']

def update_sheet(file):
    """
    Updates a specific sheet in the google sheet in accordance with the csv file."""
    global scope
    global gc
    global sheet
    global sheet_lock
    sheet_lock.acquire()
    try:
        sheetName = ""
        if file == get_log_path():
            sheetName = "Logs"
        elif file == get_current_students_path():
            sheetName = "Current Entries"
        elif file == get_room_path():
            sheetName = "Room Settings"
        elif file == get_items_path():
            sheetName = "Item Settings"
        # Open the Google Sheet
        sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1GoRyPMKROvDTHMwj3MQRT7pRbovElxDQUoMRK7_0jUM/edit?usp=sharing")    
        worksheet = sheet.worksheet(sheetName)
        worksheet.clear()
        # Read the CSV file data

        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
    finally:
        sheet_lock.release()

    # Upload CSV data to the first sheet of the Google Sheet
    worksheet.update('A1', data)

def update_sheets():
    """Updates all sheets in the google sheet in accordance with the csv files."""
    update_sheet(get_current_students_path())
    update_sheet(get_log_path())
    update_sheet(get_room_path())
    update_sheet(get_items_path())
    update_weekly_log_sheet()

def retrieve_sheet(sheet_name):
    """Synchronizes the local csv file with the respective google sheet."""
    global scope
    global gc
    global sheet
    global sheet_lock
    sheet_lock.acquire()
    try:
        print("Retrieving: " + sheet_name)
        sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1GoRyPMKROvDTHMwj3MQRT7pRbovElxDQUoMRK7_0jUM/edit?usp=sharing").worksheet(sheet_name)


        list_of_lists = sheet.get_all_values()
        fileName = ""

        if sheet_name == "Logs":
            fileName = get_log_path()
        elif sheet_name == "Current Entries":
            fileName = get_current_students_path()
            update_weekly_log_sheet()
        elif sheet_name == "Room Settings":
            fileName = get_room_path()
        elif sheet_name == "Item Settings":
            fileName = get_items_path()


        with open(fileName, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(list_of_lists)
    finally:
        sheet_lock.release()

def retrieve_all():
    """Synchronizes all local csv files with the respective google sheets."""
    retrieve_sheet("Current Entries")
    retrieve_sheet("Logs")
    retrieve_sheet("Room Settings")
    retrieve_sheet("Item Settings")
    print("Done retrieving")

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

def sheet_exists(service, sheet_title,      spreadsheet_id="1GoRyPMKROvDTHMwj3MQRT7pRbovElxDQUoMRK7_0jUM"):
    """Checks if a sheet exists in the google sheet.
    Args:
        service: The google sheet service
        sheet_title: The title of the sheet to check
        spreadsheet_id: The id of the google sheet
    Returns:
        bool: True if the sheet exists, False otherwise
    """
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')

    # Check if the sheet already exists
    for sheet in sheets:
        if sheet.get("properties", {}).get("title", "") == sheet_title:
            return True
    return False
    
def create_new_sheet(sheet_name):
    """Creates a new sheet in the google sheet.
    Args:
        sheet_name: The name of the sheet to create
    Returns:
        str: The id of the created sheet
    """
    service = build('sheets', 'v4', credentials=creds)

    # Check if sheet for this week already exists
    if sheet_exists(service, sheet_name):
        print(f"Sheet for the week ({sheet_name}) already exists.")
        return

    # Specify the properties of the new sheet
    spreadsheet_body = {
        'properties': {
            'title': sheet_name
        }
    }

    # Create the sheet and get the response
    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()

    # Return the created sheet's ID
    return response.get('spreadsheetId')

def update_weekly_log_sheet():
    global gc

    # Get the formatted date for the current week's Monday
    sheet_name = formatted_monday_date()
    spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1GoRyPMKROvDTHMwj3MQRT7pRbovElxDQUoMRK7_0jUM/edit?usp=sharing")

    # Check if the sheet for the current week already exists
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        # Create a new worksheet if it doesn't exist
        spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")
        worksheet = spreadsheet.worksheet(sheet_name)

    # Get entries from the current week
    current_week_entries = get_entries_from_current_week()

    # Clear the worksheet and update it with the current week's entries
    worksheet.clear()
    worksheet.update('A1', [headers] + current_week_entries)  # Assuming 'headers' is defined and contains the header row

