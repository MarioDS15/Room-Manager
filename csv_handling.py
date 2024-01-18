import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
from data_loader import *


def upload_csv_to_sheet(csv_file_path, sheet_name = None):
    # Define the scope of the application
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    # Load credentials from the downloaded JSON key file
    creds = ServiceAccountCredentials.from_json_keyfile_name('client.json', scopes=scope)

    # Authorize the credentials with gspread
    gc = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1GoRyPMKROvDTHMwj3MQRT7pRbovElxDQUoMRK7_0jUM/edit?usp=sharing").sheet1

    sheet.clear()
    # Read the CSV file data

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    # Upload CSV data to the first sheet of the Google Sheet
    sheet.update('A1', data)

#upload_csv_to_sheet(CURRENT_STUDENTS_FILE, "Sheet1")
