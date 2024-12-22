import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import shutil
from datetime import datetime


# Step 1: Define the scope and authenticate using the service account
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Authenticate using the service account JSON file
credentials = ServiceAccountCredentials.from_json_keyfile_name('Fileshaker\sheet-reader.json', scope)
client = gspread.authorize(credentials)

# Open the Google Sheet by its URL
sheet_url = 'https://docs.google.com/spreadsheets/d/12_sh_2ncWKpIbKKxkXBNCdcmMVdaXf-NUww7MotNxRc/edit?usp=sharing'  # Replace with your sheet URL
sheet = client.open_by_url(sheet_url).sheet1

# Step 2: Read current names, new folder names, and other relevant columns from the sheet
data = sheet.get_all_records()  # Get all rows as a list of dictionaries
name_folder_mapping = {row['VPN']: row['Primary Name'] for row in data}

# Step : Get today's date in the desired format
today_date = datetime.now().strftime("%Y-%m-%d")  # Ensure this is declared here

# Step : Define the folder paths
source_folder_path = 'Fileshaker\files-to-rename'  # Folder containing files
output_base_path = 'Fileshaker\files-shaked'  # Base folder for outputs


# Step 3: Loop through files in the 'files-to-rename' directory
folder_path = 'Fileshaker\files-to-rename'  # Folder containing files

for row in data:
    vpn = str(row['VPN']).lower()  # Convert VPN to string
    primary_name = row['Primary Name']  # The new name for the first matching file
    alt_folder_name = row['Alt Folder Name']  # The folder to move the remaining files to

    # Step 4: Search for files in the folder that contain the VPN in their name
    files_to_process = []

    for filename in os.listdir(folder_path):
        current_file_path = os.path.join(folder_path, filename)

        # Skip directories (only process files)
        if os.path.isdir(current_file_path):
            continue

        # If the VPN (converted to string) is found in the filename, add it to the list of files to process
        if vpn in filename.lower():
            files_to_process.append(current_file_path)

    # Step 5: Sort the files (e.g., by filename)
    files_to_process.sort()  # Modify this sorting criterion as needed

    # Step 7: Create output folders
    primary_folder = os.path.join('/Users/amirali/Library/Mobile Documents/com~apple~CloudDocs/Python Projects/Renamer/files-to-rename', f"Primary_{today_date}")
    alt_folder = os.path.join('/Users/amirali/Library/Mobile Documents/com~apple~CloudDocs/Python Projects/Renamer/files-to-rename', f"Alt_{today_date}")

    os.makedirs(primary_folder, exist_ok=True)
    os.makedirs(alt_folder, exist_ok=True)

    # Step 8: If there are files to process, handle renaming and moving
    if files_to_process:
        # Rename and move the first file to the "Primary" folder
        first_file = files_to_process[0]
        first_file_name = os.path.basename(first_file)

        # Extract file extension
        file_extension = os.path.splitext(first_file_name)[1]

        # Rename and move the first file
        new_primary_path = os.path.join(primary_folder, primary_name + file_extension)
        os.rename(first_file, new_primary_path)
        print(f"Moved '{first_file_name}' to '{new_primary_path}'")

        # Rename and move the remaining files to the "Alt" folder
        for index, file_path in enumerate(files_to_process[1:], start=1):
            file_name = os.path.basename(file_path)
            alt_name = f"{primary_name}_alt{index}{file_extension}"
            new_alt_file_path = os.path.join(alt_folder, alt_name)

            os.rename(file_path, new_alt_file_path)
            print(f"Moved '{file_name}' to '{new_alt_file_path}'")
    else:
        print(f"No files found matching VPN '{vpn}' in folder '{source_folder_path}'")
