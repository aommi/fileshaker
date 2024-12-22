import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pathlib import Path
#from msal import PublicClientApplication #this is for using oneDrive


# Step 1: Define the scope and authenticate for both sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Define credentials paths
base_dir = Path('Fileshaker')  # Replace with your base directory if needed
credentials_path = base_dir / 'secret' / 'sheet-reader.json'
renamer_credentials_path = base_dir / 'secret' / 'sheet-reader.json'
logger_credentials_path = base_dir / 'secret' / 'sheet-writer-key.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(str(credentials_path), scope)
client = gspread.authorize(credentials)

# Authenticate for Renamer Sheet
renamer_credentials = ServiceAccountCredentials.from_json_keyfile_name(str(renamer_credentials_path), scope)
renamer_client = gspread.authorize(renamer_credentials)

# Authenticate for Shake Logger Sheet
logger_credentials = ServiceAccountCredentials.from_json_keyfile_name(str(logger_credentials_path), scope)
logger_client = gspread.authorize(logger_credentials)

# Step 2: Open the sheets by their URLs
renamer_sheet_url = 'https://docs.google.com/spreadsheets/d/12_sh_2ncWKpIbKKxkXBNCdcmMVdaXf-NUww7MotNxRc/edit?usp=sharing'
logger_sheet_url = 'https://docs.google.com/spreadsheets/d/1fU1YOUv_DAzIb0PBvx__KfHoZ2EqXymOqnqCgrUMxJc/edit?usp=sharing'

# Open sheets
renamer_sheet = renamer_client.open_by_url(renamer_sheet_url).sheet1
logger_sheet = logger_client.open_by_url(logger_sheet_url).sheet1

# Step 3: Read data from the Renamer Sheet
data = renamer_sheet.get_all_records()  # Get all rows as a list of dictionaries

# Step 4: Prepare file paths and date
source_folder_path = base_dir  / 'files-to-rename' 
today_date = datetime.now().strftime("%Y-%m-%d")

# Step 5: Loop through the rows in the Renamer Sheet
for row in data:
    vpn = str(row['VPN']).lower()  # Convert VPN to string
    primary_name = row['Primary Name']
    notes = row.get('Notes', '')  # Notes column from the Renamer sheet (default to empty)

    # Skip processing if VPN is blank
    if not vpn:
        print("Skipping row with blank VPN value.")
        continue
    
    # Search for files containing the VPN in their name
    files_to_process = [
        source_folder_path / filename
        for filename in os.listdir(source_folder_path)
        if vpn in filename.lower() and not (source_folder_path / filename).is_dir()
    ]
     # Skip processing if no matching files are found
    if not files_to_process:
        print(f"No matching files found for VPN '{vpn}'. Skipping processing.")
        continue
    # Sort the files
    files_to_process.sort()

    # Create output folders
    primary_folder = source_folder_path / f"Primary_{today_date}"
    alt_folder = source_folder_path / f"Alt_{today_date}"

    primary_folder.mkdir(parents=True, exist_ok=True)
    alt_folder.mkdir(parents=True, exist_ok=True)

    # Initialize logging variables
    is_primary_moved = False
    num_alts = 0
    alt_folder_name_logged = ""

    if files_to_process:
        # Rename and move the first file
        first_file = files_to_process[0]
        file_extension = first_file.suffix
        new_primary_path = primary_folder / (primary_name + file_extension)
        first_file.rename(new_primary_path)
        is_primary_moved = True
        print(f"Primary file '{first_file.name}' moved to '{primary_folder}'")

        # Process the remaining files (Alt files)
        for index, file_path in enumerate(files_to_process[1:], start=1):
            file_extension = file_path.suffix
            alt_name = f"{primary_name}_alt{index}{file_extension}"
            new_alt_file_path = alt_folder / alt_name
            file_path.rename(new_alt_file_path)
            num_alts += 1
            alt_folder_name_logged = str(alt_folder)  # Record the Alt folder name

        # Print the Alt folder name after processing all alts
        print(f"Alt files for VPN '{vpn}' are moved to folder: {alt_folder}")

    # Log actions to the Shake Logger Sheet
    logger_sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Date
        vpn,                                           # Search key
        primary_name,                                  # Primary Name
        "Yes" if is_primary_moved else "No",           # Is Primary moved
        num_alts,                                      # Number of Alts
        notes,                                         # Notes
        str(primary_folder) if is_primary_moved else "",  # Primary folder
        alt_folder_name_logged,                        # Alt Folder Name
    ])
