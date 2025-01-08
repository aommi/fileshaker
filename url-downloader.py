import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import os
from datetime import datetime
from pathlib import Path
import time
from collections import defaultdict

# Step 1: Define the scope and authenticate for both sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Define credentials paths
base_dir = Path("C:/Python Projects")  # Replace with your base directory if needed
credentials_path = base_dir / "secret"
downloader_credentials_path = credentials_path / "sheet-reader-key.json"
logger_credentials_path = credentials_path / "sheet-writer-key.json"

# Authenticate for Downloader Sheet
downloader_credentials = ServiceAccountCredentials.from_json_keyfile_name(str(downloader_credentials_path), scope)
downloader_client = gspread.authorize(downloader_credentials)
downloader_sheet_url = "https://docs.google.com/spreadsheets/d/1DubHPcNpeLRdXWDfw8qBDw30Ia-Ve3ZUlmEP7S7yd1Y/edit?usp=sharing"

# Directory to save downloaded files
DOWNLOAD_DIR = "files-downloaded"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Open the Google Sheet
sheet = downloader_client.open_by_url(downloader_sheet_url).sheet1

# Get data from relevant columns
data = sheet.get_all_records()

# Track ALT file counts per ProductID_Colour
alt_file_count = defaultdict(int)

# Download files based on URL and naming conventions
for index, record in enumerate(data):
    url = record.get("URL")
    product_id_colour = record.get("ProductID_Colour")
    asset_type = record.get("Image Type")

    if url and url.startswith("http"):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            file_extension = os.path.splitext(url)[-1] if '.' in os.path.basename(url) else '.bin'

            if asset_type and asset_type.lower() == "primary" and product_id_colour:
                filename = os.path.join(DOWNLOAD_DIR, f"{product_id_colour}{file_extension}")
            elif asset_type and asset_type.lower() == "alt" and product_id_colour:
                alt_file_count[product_id_colour] += 1
                filename = os.path.join(DOWNLOAD_DIR, f"{product_id_colour}_ALT-{alt_file_count[product_id_colour]}{file_extension}")
            else:
                filename = os.path.join(DOWNLOAD_DIR, f"file_{index + 1}{file_extension}")

            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Downloaded: {url} to {filename}")
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")
    else:
        print(f"Invalid URL or missing URL in record: {record}")