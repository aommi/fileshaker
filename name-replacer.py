import os
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Step 1: Define the scope and authenticate
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
base_dir = Path('C:/Python Projects/fileshaker')  # Base directory
asset_dir = base_dir/Path('Assets Processed/')  # Base directory
credentials_path = base_dir / 'secret' / 'sheet-reader-key.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(str(credentials_path), scope)
client = gspread.authorize(credentials)

# Step 2: Open the Renamer Sheet by URL
renamer_sheet_url = 'https://docs.google.com/spreadsheets/d/12_sh_2ncWKpIbKKxkXBNCdcmMVdaXf-NUww7MotNxRc/edit?usp=sharing'
renamer_sheet = client.open_by_url(renamer_sheet_url).get_worksheet_by_id('1878798757')

# Step 3: Read data from the Renamer Sheet
data = renamer_sheet.get_all_records()
print(data)

# Step 4: Prepare file paths
source_folder_path = asset_dir /'files-to-uppercase'

# Step 5: Rename files based on the sheet
for row in data:
    old_suffix = row['old-suffix']  # Replace 'Column 1' with actual column name
    new_suffix = row['new-suffix']  # Replace 'Column 2' with actual column name

    # Skip processing if old_suffix is blank
    if not old_suffix:
        print("Skipping row with blank old suffix value.")
        continue

    # Search for files containing the old_suffix in their name
    for filename in os.listdir(source_folder_path):
        file_path = source_folder_path / filename
        if old_suffix in filename and file_path.is_file():
            # Replace old_suffix with new_suffix in the filename
            new_filename = filename.replace(old_suffix, new_suffix)
            new_file_path = source_folder_path / new_filename
            os.rename(file_path, new_file_path)
            print(f"Renamed: {filename} -> {new_filename}")
