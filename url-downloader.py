import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import os
from datetime import datetime
from pathlib import Path
import time
from collections import defaultdict
import re  # sanitizing filenames

# Step 1: Define the scope and authenticate for both sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Define credentials paths
base_dir = Path("C:/Python-Projects/fileshaker")  # Replace with your base directory if needed
credentials_path = base_dir / "secret"
downloader_credentials_path = credentials_path / "sheet-reader-key.json"
logger_credentials_path = credentials_path / "sheet-writer-key.json"

# Authenticate for Downloader Sheet
downloader_credentials = ServiceAccountCredentials.from_json_keyfile_name(str(downloader_credentials_path), scope)
downloader_client = gspread.authorize(downloader_credentials)
downloader_sheet_url = "https://docs.google.com/spreadsheets/d/1DubHPcNpeLRdXWDfw8qBDw30Ia-Ve3ZUlmEP7S7yd1Y/edit?usp=sharing"

# Directory to save downloaded files
DOWNLOAD_DIR = "assets/files-downloaded"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Open the Google Sheet
sheet = downloader_client.open_by_url(downloader_sheet_url).sheet1

# Get data from relevant columns
data = sheet.get_all_records()

# Track ALT file counts per ProductID_Colour
alt_file_count = defaultdict(int)

def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filenames."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def try_download_with_session(url: str) -> requests.Response:
    """Attempt to download with session if normal request fails."""
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    return session.get(url, headers=headers, stream=True, allow_redirects=True)

def get_extension_from_response(response):
    """Get file extension from Content-Type header or default to .jpg"""
    content_type = response.headers.get('Content-Type', '')
    if 'image/jpeg' in content_type or 'image/jpg' in content_type:
        return '.jpg'
    elif 'image/png' in content_type:
        return '.png'
    elif 'image/tiff' in content_type:
        return '.tif'
    return '.jpg'

def download_file(url: str, filepath: str) -> bool:
    """Download file with fallback to session-based download if direct download fails."""
    try:
        # First attempt - direct download (unchanged)
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.RequestException as e:
        # Only handle extension in fallback case
        try:
            response = try_download_with_session(url)
            response.raise_for_status()
            
            # Only update extension if the original extension is missing
            if not os.path.splitext(filepath)[1]:
                new_ext = get_extension_from_response(response)
                filepath = os.path.splitext(filepath)[0] + new_ext
                
        except requests.RequestException as e:
            print(f"Both download attempts failed for {url}: {e}")
            return False

    # If we got here, one of the download attempts succeeded
    with open(filepath, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    return True

# Modify the main download loop
for index, record in enumerate(data):
    url = record.get("URL")
    product_id_colour = record.get("ProductID_Colour")
    asset_type = record.get("Image Type")
    vpn = record.get("vpn")

    if url and url.startswith("http"):
        try:
            file_extension = os.path.splitext(url.split('?')[0])[-1]
            
            if asset_type and asset_type.lower() == "primary" and product_id_colour:
                filename = f"{product_id_colour}{file_extension}"
            elif asset_type and asset_type.lower() == "alt" and product_id_colour:
                alt_file_count[product_id_colour] += 1
                filename = f"{product_id_colour}_ALT-{alt_file_count[product_id_colour]}{file_extension}"
            else:
                filename = f"file_{index + 1}{file_extension}"

            filename = sanitize_filename(filename)
            filepath = os.path.join(DOWNLOAD_DIR, filename)

            if download_file(url, filepath):
                print(f"Successfully downloaded: {url} to {filepath}")
            else:
                print(f"Failed to download: {url}")

        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
    else:
        print(f"Invalid URL or missing URL in record: {record}")
