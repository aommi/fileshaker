# log-in-sheet.py

import time
from datetime import datetime

def log_in_sheet(logger_sheet, vpn, primary_name, is_primary_moved, num_alts, notes, primary_folder, alt_folder_name_logged, eta, delay):
    logger_sheet.append_row([
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
    time.sleep(delay)