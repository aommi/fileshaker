import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import time

# Define a function to log the time taken for each step
def log_time(operation, start_time):
    end_time = time.time()
    print(f"{operation} took {end_time - start_time:.2f} seconds")
    return end_time

# Step 1: Define the scope and authenticate for both sheets
scope = ['https://www.googleapis.com/auth/drive']

# Define credentials paths
base_dir = Path('C:/python-projects/fileshaker')  # Replace with your base directory if needed
#base_dir=Path('/Users/amirali/Library/Mobile Documents/com~apple~CloudDocs/Python Projects/fileshaker') #use for mac
credentials_path = Path(base_dir / 'secret')
renamer_credentials_path = Path(credentials_path / 'sheet-reader-key.json')

# Step 2: Authenticate for Renamer Sheet
start_time = time.time()
renamer_credentials = ServiceAccountCredentials.from_json_keyfile_name(str(renamer_credentials_path), scope)
renamer_client = gspread.authorize(renamer_credentials)
start_time = log_time("Authentication", start_time)

# Step 3: Open the sheets by their IDs
spreadsheet_id = '12_sh_2ncWKpIbKKxkXBNCdcmMVdaXf-NUww7MotNxRc'
start_time = time.time()
renamer_sheet = renamer_client.open_by_key(spreadsheet_id).get_worksheet_by_id(0)
start_time = log_time("API Call Preparation and Response", start_time)

# Step 4: Read data from the Renamer Sheet
start_time = time.time()
data = renamer_sheet.get_all_records()  # Get all rows as a list of dictionaries
start_time = log_time("Data Fetching", start_time)

# Step 5: Print results
start_time = time.time()
print(data[0].keys())
log_time("Printing Results", start_time)