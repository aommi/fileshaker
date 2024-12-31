import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#from datetime import datetime
from pathlib import Path
import time


# Step 1: Define the scope and authenticate for both sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Define credentials paths
base_dir = Path('C:/Python Projects')  # Replace with your base directory if needed
credentials_path = base_dir / 'secret'
renamer_credentials_path = credentials_path / 'sheet-reader-key.json'
logger_credentials_path = credentials_path /  'sheet-writer-key.json'



# Authenticate for Renamer Sheet
renamer_credentials = ServiceAccountCredentials.from_json_keyfile_name(str(renamer_credentials_path), scope)
renamer_client = gspread.authorize(renamer_credentials)

# Authenticate for Shake Logger Sheet
#logger_credentials = ServiceAccountCredentials.from_json_keyfile_name(str(logger_credentials_path), scope)
#logger_client = gspread.authorize(logger_credentials)

# Step 2: Open the sheets by their URLs
renamer_sheet_url = 'https://docs.google.com/spreadsheets/d/12_sh_2ncWKpIbKKxkXBNCdcmMVdaXf-NUww7MotNxRc/edit?usp=sharing'
#logger_sheet_url = 'https://docs.google.com/spreadsheets/d/1fU1YOUv_DAzIb0PBvx__KfHoZ2EqXymOqnqCgrUMxJc/edit?usp=sharing'

# Open sheets
renamer_sheet = renamer_client.open_by_url(renamer_sheet_url).sheet1
#logger_sheet = logger_client.open_by_url(logger_sheet_url).sheet1

# Step 3: Read data from the Renamer Sheet
data = renamer_sheet.get_all_records()  # Get all rows as a list of dictionaries
#print(data[0].keys())


# Step 4: Prepare file paths and date
source_folder_path = base_dir  / 'Assets Processed'/'files-to-rename'/'SWATCHES' 
#today_date = datetime.now().strftime("%Y-%m-%d")

# Step 5: Loop through the rows in the Renamer Sheet
for row in data:
    vpn = str(row['VPN']).lower()  # Convert VPN to string
    alt_vpn = str(row['alt-VPN']).lower()
    primary_name = row['Primary Name']
    # notes = row.get('Notes', '')  # Notes column from the Renamer sheet (default to empty)
    # eta = row.get('ETA', '')

    # Skip processing if VPN is blank
    if not vpn:
        print("Skipping row with blank VPN value.")
        continue
    
    # Search for files containing the VPN in their name
    files_to_process = [
        source_folder_path / filename
        for filename in os.listdir(source_folder_path)
        if (vpn in filename.lower() or alt_vpn in filename.lower()) and not (source_folder_path / filename).is_dir()
    ]
    
    # Skip processing if no matching files are found
    if not files_to_process:
        print(f"No matching files found for VPN '{vpn}'. Skipping processing.")
        continue

    if files_to_process:
        # Rename the first file
        first_file = files_to_process[0]
        file_extension = first_file.suffix
        new_file_path = first_file.with_name(f"{primary_name}_SWATCH{file_extension}")
        first_file.rename(new_file_path)
        print(f"Renamed '{first_file.name}' to '{new_file_path.name}'")