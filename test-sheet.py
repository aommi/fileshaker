import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
#from msal import PublicClientApplication #this is for using oneDrive
# # Configurable setting

# Step 1: Define the scope and authenticate for both sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Define credentials paths
base_dir=Path('/Users/amirali/Library/Mobile Documents/com~apple~CloudDocs/Python Projects/fileshaker') #use for mac
#base_dir = Path('C:/python-projects/fileshaker')  # Replace with your base directory if needed #use for windows
credentials_path = Path(base_dir / 'secret')
renamer_credentials_path = Path(credentials_path / 'sheet-reader-key.json')


# Authenticate for Renamer Sheet
renamer_credentials = ServiceAccountCredentials.from_json_keyfile_name(str(renamer_credentials_path), scope)
renamer_client = gspread.authorize(renamer_credentials)



# Step 2: Open the sheets by their URLs
renamer_sheet_url = 'https://docs.google.com/spreadsheets/d/12_sh_2ncWKpIbKKxkXBNCdcmMVdaXf-NUww7MotNxRc/'

# Open sheets
renamer_sheet = renamer_client.open_by_url(renamer_sheet_url).get_worksheet_by_id('0')

# Step 3: Read data from the Renamer Sheet
data = renamer_sheet.get_all_records()  # Get all rows as a list of dictionaries
print(data[0].keys())