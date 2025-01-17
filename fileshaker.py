import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pathlib import Path
import time
#from msal import PublicClientApplication #this is for using oneDrive
# # Configurable setting
SKIP_IF_SINGLE_ALT = False  # Set to False to disable this condition
DELAY=1.1
alphabet=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","P","Q","R","S","T","U","V","W","X","Y","Z"]

# Step 1: Define the scope and authenticate for both sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Define credentials paths
base_dir = Path('C:/Python Projects/fileshaker')  # Replace with your base directory if needed
credentials_path = base_dir / 'secret'
renamer_credentials_path = credentials_path / 'sheet-reader-key.json'
logger_credentials_path = credentials_path /  'sheet-writer-key.json'



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
#print(data[0].keys())


# Step 4: Prepare file paths and date
source_folder_path = base_dir  / 'Assets Processed'/'files-to-rename' 
today_date = datetime.now().strftime("%Y-%m-%d")

# Step 5: Loop through the rows in the Renamer Sheet
for row in data:
    vpn = str(row['VPN']).lower()  # Convert VPN to string
    alt_vpn=str(row['alt-VPN']).lower()
    primary_name = row['Primary Name']
    notes = row.get('Notes', '')  # Notes column from the Renamer sheet (default to empty)
    eta=row.get('ETA','')

    # Skip processing if VPN is blank
    if not vpn:
        print("Skipping row with blank VPN value.")
        continue
    
    # Search for files containing the VPN in their name
    files_to_process = [
        source_folder_path / filename
        for filename in os.listdir(source_folder_path)
        if (vpn in filename.lower() or alt_vpn in filename.lower())and not (source_folder_path / filename).is_dir()
    ]
    
    # Skip processing if no matching files are found
    if not files_to_process:
        print(f"No matching files found for VPN '{vpn}'. Skipping processing.")
        continue

    # Sort the files
    #files_to_process.sort()
    
    files_to_process.sort(key=lambda filepath: (
    0 if 'model_1' in str(filepath).lower()
    else 1 if 'product_1' in str(filepath).lower() else
    2, filepath
))
    """
    files_to_process.sort(key=lambda filepath: (
        0 if 'A1' in str(filepath).lower()
        else 1 if 'E1' in str(filepath).lower()
        else 1 if 'D1' in str(filepath).lower()
        else 1 if 'C1' in str(filepath).lower()
        else
        2, filepath
))
"""
    # Handle case where there is only one matching file
    if SKIP_IF_SINGLE_ALT and len(files_to_process) == 1:
        single_alt_folder = source_folder_path / f"Single_ALT_{today_date}"
        single_alt_folder.mkdir(parents=True, exist_ok=True)
        
        single_file = files_to_process[0]
        new_single_file_path = single_alt_folder / single_file.name
        single_file.rename(new_single_file_path)
        
        print(f"Only one matching file found for VPN '{vpn}'. Moved to '{single_alt_folder}'.")
        
        # Log this action
        logger_sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Date
            vpn,                                           # Search key
            primary_name,                                  # Primary Name
            "Skipped (Single ALT)",                       # Status
            0,                                            # Number of Alts
            notes,                                        # Notes
            "",                                           # Primary folder
            str(single_alt_folder),                        # Single Alt Folder Name
            eta                                             #Current ETA Date
        ])
        time.sleep(DELAY)
        continue

    # Create output folders
    primary_folder = source_folder_path / f"Primary_{today_date}"
    alt_folder = source_folder_path / f"ALT_{today_date}"

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
            alt_name = f"{primary_name}_ALT_{alphabet[index-1]}{file_extension}"
            new_alt_file_path = alt_folder / alt_name
            file_path.rename(new_alt_file_path)
            num_alts += 1
            alt_folder_name_logged = str(alt_folder)  # Record the Alt folder name

        # Print the Alt folder name after processing all alts
        print(f"ALT files for VPN '{vpn}' are moved to folder: {alt_folder}")

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
        eta                                            # Current ETA Date
    ])
    time.sleep(DELAY)
