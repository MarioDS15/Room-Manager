import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import os
import csv
from data_loader import *
import socket
from datetime import datetime, timedelta
from data_handling import *

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('client.json', scopes=scope)

# Authorize the credentials with gspread
gc = gspread.authorize(creds)


def update_sheet(file):
    """
    Updates a specific sheet in the google sheet in accordance with the csv file."""
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
    """Updates all sheets in the google sheet in accordance with the csv files."""
    update_sheet(CURRENT_STUDENTS_FILE)
    update_sheet(LOG_FILE)
    update_sheet(ROOM_FILE)
    update_sheet(ITEMS_FILE)

def retrieve_sheet(sheet_name):
    """Synchronizes the local csv file with the respective google sheet."""
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

