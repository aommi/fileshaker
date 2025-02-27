import os
from datetime import datetime
from pathlib import Path
import time
from dotenv import load_dotenv
from sheet_utils import SheetUtils
from style_assets import StyleAssets  
from data_pre_processor import DataPreProcessor

load_dotenv()

# Configuration
DELAY = 1.1
CUSTOM_SORT = True  # Set this to True for custom sorting, False for default sorting
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","P","Q","R","S","T","U","V","W","X","Y","Z"]
base_dir = Path(os.getenv('BASE_DIR'))
source_folder_path = base_dir / os.getenv('SHAKER_ASSET_DIR')
output_folder_path = base_dir / 'assets' / 'files-shaked'
today_date = datetime.now().strftime("%Y-%m-%d")

# Initialize SheetUtils
sheet_utils = SheetUtils()
data_pre_processor = DataPreProcessor()

# Sheet keys and GIDs
shaker_input_key = os.getenv('SHAKER_INPUT_SHEET_KEY')
shaker_logger_key = os.getenv('SHAKER_LOGGER_SHEET_KEY')
shaker_input_gid = int(os.getenv('SHAKER_INPUT_WORKSHEET_GID'))
shaker_logger_gid = int(os.getenv('SHAKER_LOGGER_WORKSHEET_GID'))

def read_shaker_input():
    return sheet_utils.read_sheet_data(sheet_utils.reader_client, shaker_input_key, shaker_input_gid)

def log_to_shaker_logger(row_data):
    sheet_utils.write_to_sheet(sheet_utils.writer_client, shaker_logger_key, shaker_logger_gid, row_data)

def create_output_folders():
    primary_folder = output_folder_path / f"Primary_{today_date}"
    alt_folder = output_folder_path / f"ALT_{today_date}"
    primary_folder.mkdir(parents=True, exist_ok=True)
    alt_folder.mkdir(parents=True, exist_ok=True)
    return primary_folder, alt_folder

def process_files(prepared_data):
    shaker = StyleAssets(
        source_folder_path=source_folder_path,
        output_folder_path=output_folder_path,
        today_date=today_date,
        alphabet=alphabet,
        custom_sort=CUSTOM_SORT
    )

    for data in prepared_data:
        vpn, alt_vpn, primary_name, notes, eta = data
        files_to_process = shaker.find_assets(vpn, alt_vpn)
        if not files_to_process:
            print(f"No matching files found for VPN '{vpn}'. Skipping processing.")
            continue

        files_to_process = shaker.sort_assets(files_to_process)

        primary_folder, alt_folder = create_output_folders()
        is_primary_moved, num_alts, alt_folder_name_logged = shaker.move_assets(files_to_process, vpn, primary_name, primary_folder, alt_folder)

        log_to_shaker_logger([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            vpn,
            primary_name,
            "Yes" if is_primary_moved else "No",
            num_alts,
            notes,
            str(primary_folder) if is_primary_moved else "",
            alt_folder_name_logged,
            eta
        ])

def main():
    data = read_shaker_input()
    print(data[0].keys())
    process = 'shaker'  # Change this to 'download' for download processing
    prepared_data = data_pre_processor.prepare_data(data, process)
    process_files(prepared_data)

if __name__ == "__main__":
    main()