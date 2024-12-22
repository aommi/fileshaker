from pathlib import Path
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import shutil
from datetime import datetime

# Step 1: Define the scope and authenticate using the service account
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Authenticate using the service account JSON file
credentials_path = Path('Fileshaker') / 'sheet-reader.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(credentials)

# Open the Google Sheet by its URL
sheet_url = 'https://docs.google.com/spreadsheets/d/12_sh_2ncWKpIbKKxkXBNCdcmMVdaXf-NUww7MotNxRc/edit?usp=sharing'
sheet = client.open_by_url(sheet_url).sheet1

# Step 2: Read current names, new folder names, and other relevant columns from the sheet
data = sheet.get_all_records()
name_folder_mapping = {row['VPN']: row['Primary Name'] for row in data}

# Step : Get today's date in the desired format
today_date = datetime.now().strftime("%Y-%m-%d")

# Step : Define the folder paths
source_folder_path = Path('Fileshaker') / 'files-to-rename'
output_base_path = Path('Fileshaker') / 'files-shaked'

# Step 3: Loop through files in the 'files-to-rename' directory
folder_path = source_folder_path

for row in data:
    vpn = str(row['VPN']).lower()
    primary_name = row['Primary Name']
    alt_folder_name = row['Alt Folder Name']

    # Step 4: Search for files in the folder that contain the VPN in their name
    files_to_process = []

    for filename in os.listdir(folder_path):
        current_file_path = folder_path / filename

        # Skip directories
        if current_file_path.is_dir():
            continue

        # Add files that match the VPN
        if vpn in filename.lower():
            files_to_process.append(current_file_path)

    # Step 5: Sort the files
    files_to_process.sort()

    # Step 7: Create output folders
    primary_folder = output_base_path / f"Primary_{today_date}"
    alt_folder = output_base_path / f"Alt_{today_date}"

    primary_folder.mkdir(parents=True, exist_ok=True)
    alt_folder.mkdir(parents=True, exist_ok=True)

    # Step 8: Handle renaming and moving
    if files_to_process:
        first_file = files_to_process[0]
        file_extension = first_file.suffix

        # Rename and move the primary file
        new_primary_path = primary_folder / f"{primary_name}{file_extension}"
        first_file.rename(new_primary_path)
        print(f"Moved '{first_file.name}' to '{new_primary_path}'")

        # Rename and move the remaining files
        for index, file_path in enumerate(files_to_process[1:], start=1):
            alt_name = f"{primary_name}_alt{index}{file_extension}"
            new_alt_file_path = alt_folder / alt_name
            file_path.rename(new_alt_file_path)
            print(f"Moved '{file_path.name}' to '{new_alt_file_path}'")
    else:
        print(f"No files found matching VPN '{vpn}' in folder '{folder_path}'")
