# config.py

from pathlib import Path

CONFIG = {
    # General Settings
    "skip_if_single_alt": False,  # Whether to skip processing if only one alternative exists
    "delay": 1.1,  # Delay between operations (in seconds)
    "alphabet": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",  # Alphabet used for ALT file naming

    # Directories
    "base_dir": Path("/Users/amirali/Library/Mobile Documents/com~apple~CloudDocs/Python Projects"),  # Base directory where all operations will occur
    "source_folder_path": Path("files-to-rename"),  # Source folder path for files to rename

    # Credential Files
    "credentials": {
        "renamer": Path("secret/sheet-reader-key.json"),  # Path to the renamer Google Sheets API credentials
        "logger": Path("secret/sheet-writer-key.json"),  # Path to the logger Google Sheets API credentials
    },

    # Spreadsheet Settings (Example: Google Sheets)
    "sheets": {
        "renamer": {
            "url": "https://docs.google.com/spreadsheets/d/12_sh_2ncWKpIbKKxkXBNCdcmMVdaXf-NUww7MotNxRc/edit?usp=sharing",
        },
        "logger": {
            "url": "https://docs.google.com/spreadsheets/d/1fU1YOUv_DAzIb0PBvx__KfHoZ2EqXymOqnqCgrUMxJc/edit?usp=sharing",
        },
    },
}