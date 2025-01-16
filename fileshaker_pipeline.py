# fileshaker_pipeline.py

from config import CONFIG
from sheet_authenticator import SheetAuthenticator
from load_sheet_data import load_sheet_data
from search_for_files import search_for_files
from sort_files import sort_files
from move_files import move_files
from log_in_sheet import log_in_sheet
import os
import shutil
from datetime import datetime

def main():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    renamer_authenticator = SheetAuthenticator(CONFIG["credentials"]["renamer"], scope)
    logger_authenticator = SheetAuthenticator(CONFIG["credentials"]["logger"], scope)
    renamer_client = renamer_authenticator.authenticate()
    logger_client = logger_authenticator.authenticate()

    data = load_sheet_data(renamer_client, CONFIG)
    logger_sheet = logger_client.open_by_url(CONFIG["sheets"]["logger"]["url"]).sheet1

    for row in data:
        vpn = str(row['VPN']).lower()
        alt_vpn = str(row['alt-VPN']).lower()
        primary_name = row['Primary Name']
        notes = row.get('Notes', '')
        eta = row.get('ETA', '')

        if not vpn:
            print("Skipping row with blank VPN value.")
            continue

        files_to_process = search_for_files(CONFIG["source_folder_path"], vpn, alt_vpn)

        if not files_to_process:
            print(f"No matching files found for VPN '{vpn}'. Skipping processing.")
            continue

        files_to_process = sort_files(files_to_process)

        if CONFIG["skip_if_single_alt"] and len(files_to_process) == 1:
            single_alt_folder = CONFIG["source_folder_path"] / f"Single_ALT_{datetime.now().strftime('%Y-%m-%d')}"
            single_alt_folder.mkdir(parents=True, exist_ok=True)
            single_file = files_to_process[0]
            new_single_file_path = single_alt_folder / single_file.name
            single_file.rename(new_single_file_path)
            print(f"Only one matching file found for VPN '{vpn}'. Moved to '{single_alt_folder}'")
            log_in_sheet(logger_sheet, vpn, primary_name, False, 0, notes, "", str(single_alt_folder), eta, CONFIG["delay"])
            continue

        is_primary_moved, num_alts, primary_folder, alt_folder_name_logged = move_files(CONFIG, files_to_process, primary_name, datetime.now().strftime('%Y-%m-%d'))
        log_in_sheet(logger_sheet, vpn, primary_name, is_primary_moved, num_alts, notes, primary_folder, alt_folder_name_logged, eta, CONFIG["delay"])

if __name__ == "__main__":
    main()