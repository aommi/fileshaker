# config.py

from pathlib import Path

CONFIG = {
    # General Settings
    "skip_if_single_alt": True,  # Whether to skip processing if only one alternative exists
    "delay": 1.1,  # Delay between operations (in seconds)
    "alphabet": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",  # Alphabet used for ALT file naming

    # Directories
    "base_dir": Path("Fileshaker"),  # Base directory where all operations will occur

    # Credential Files
    "credentials": {
        "renamer": "secret/sheet-reader.json",  # Path to the renamer Google Sheets API credentials
        "logger": "secret/sheet-writer-key.json",  # Path to the logger Google Sheets API credentials
    },

    # Spreadsheet Settings (Example: Google Sheets)
    "sheets": {
        "renamer": {
            "type": "google_sheets",  # Type of sheet integration (options: google_sheets, excel, etc.)
            "url": "https://docs.google.com/spreadsheets/d/12_sh_2ncWKpIbKKxkXBNCdcmMVdaXf-NUww7MotNxRc/edit?usp=sharing",
        },
        "logger": {
            "type": "google_sheets",  # Type of sheet integration (options: google_sheets, excel, etc.)
            "url": "https://docs.google.com/spreadsheets/d/1fU1YOUv_DAzIb0PBvx__KfHoZ2EqXymOqnqCgrUMxJc/edit?usp=sharing",
        },
    },

    # Folders
    "folders": {
        "source": "files-to-rename",  # Folder where files to be processed are located
    },
}

# Example paths for macOS or Windows:
# On macOS:
# "credentials": {
#     "renamer": "/Users/username/Projects/Fileshaker/secret/sheet-reader.json",
#     "logger": "/Users/username/Projects/Fileshaker/secret/sheet-writer-key.json",
# },
# "base_dir": Path("/Users/username/Projects/Fileshaker"),

# On Windows:
# "credentials": {
#     "renamer": "C:\\Users\\username\\Projects\\Fileshaker\\secret\\sheet-reader.json",
#     "logger": "C:\\Users\\username\\Projects\\Fileshaker\\secret\\sheet-writer-key.json",
# },
# "base_dir": Path("C:\\Users\\username\\Projects\\Fileshaker"),
