import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Config dictionary
CONFIG = {
    # Base directory and service-specific asset directories
    "base_dir": Path(os.getenv("BASE_DIR")),
    "asset_dirs": {
        "renamer": Path(os.getenv("RENAMER_ASSET_DIR")),
        "shaker": Path(os.getenv("SHAKER_ASSET_DIR")),
        "swatcher": Path(os.getenv("SWATCHER_ASSET_DIR")),
        "directory_search": Path(os.getenv("DIRECTORY_SEARCH_ASSET_DIR")),
    },

    # Google Sheets credentials (read-only for renamer and write-only for logger)
    "credentials": {
        "reader": Path(os.getenv("READER_CREDENTIALS")),  # For renaming sheet (read)
        "writer": Path(os.getenv("WRITER_CREDENTIALS")),   # For logger sheet (write)
    },

    # Google Sheets URLs
    "spreadsheets_list": {
        "fileshaker_input": {
            "url": os.getenv("FILESHAKER_SHEET_URL"),
            "input_sheet_id": os.getenv("FILESHAKER_INPUT_SHEET_ID"),
        },
        "renamer_input": {
            "url": os.getenv("RENAMER_SHEET_URL"),
            "input_sheet_id": os.getenv("RENAMER_INPUT_SHEET_ID"),
        },
        "shaker_logger": {
            "url": os.getenv("SHAKER_LOGGER_SHEET_URL"),
        },
        "url_downloader": {
            "url": os.getenv("URL_DOWNLOADER_SHEET_URL"),
        },
    },

    # Operational flags
    "operational_flags": {
        "skip_if_single_alt": os.getenv("SKIP_IF_SINGLE_ALT", "False").lower() == "true",  # Convert to boolean
        "delay": float(os.getenv("DELAY", 1.1)),
        "alphabet": os.getenv("ALPHABET", "A,B,C,D,E,F,G,H,I,J,K,L,M,N,P,Q,R,S,T,U,V,W,X,Y,Z").split(","),
    },
}
