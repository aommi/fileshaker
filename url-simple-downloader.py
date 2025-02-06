import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import os
from pathlib import Path
import urllib.parse

import re  # Import regex to clean filenames

# Define the scope and authenticate for sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Define credentials path
base_dir = Path("C:/Python-Projects/fileshaker")  # Adjust base directory if needed
credentials_path = base_dir / "secret/sheet-reader-key.json"

# Authenticate for Google Sheets
credentials = ServiceAccountCredentials.from_json_keyfile_name(str(credentials_path), scope)
client = gspread.authorize(credentials)

# Open the Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1DubHPcNpeLRdXWDfw8qBDw30Ia-Ve3ZUlmEP7S7yd1Y/edit?usp=sharing"
sheet = client.open_by_url(sheet_url).sheet1

# Directory to save downloaded files
DOWNLOAD_DIR = "assets/files-downloaded"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filenames."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Get data from sheet
data = sheet.get_all_records()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",  # Mimic a browser
    "Cookie": "JSESSIONID=8p-kGAqQMG6udtJg_aY_zAioE1Rb_LLUETZQ6LCh.rocdmhmmp01"
}


# Download files
for record in data:
    url = record.get("URL")
    if url and url.startswith("http"):
        try:
            #response = requests.get(url, stream=True)
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()
            
                        # Try to get filename from Content-Disposition
            content_disp = response.headers.get("Content-Disposition")
            if content_disp:
                match = re.search(r'filename\*?=(?:utf-8\'\')?(.+)', content_disp, re.IGNORECASE)
                if match:
                    filename = urllib.parse.unquote(match.group(1))  # Decode URL encoding
                else:
                    filename = os.path.basename(url.split('?')[0])  # Fallback to URL-based name
            else:
                filename = os.path.basename(url.split('?')[0])  # Default if no header

            # Ensure filename has an extension
            if "." not in filename:
                filename += ".jpg"  # Default to .jpg (change if needed)

            filepath = os.path.join(DOWNLOAD_DIR, filename)

            # Save the file
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"Downloaded: {url} as {filename}")
            #filename = sanitize_filename(os.path.basename(url.split('?')[0]))  # Get filename from URL
            #filepath = os.path.join(DOWNLOAD_DIR, filename)
            
            
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")
    else:
        print(f"Invalid or missing URL in record: {record}")