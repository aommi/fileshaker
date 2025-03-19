import functions_framework
from google.cloud import storage
import requests
import os
from datetime import datetime
import io
import zipfile
import gspread
from google.oauth2 import service_account
from concurrent.futures import ThreadPoolExecutor
import re
from itertools import groupby

BUCKET_NAME = "your-bucket-name"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1DubHPcNpeLRdXWDfw8qBDw30Ia-Ve3ZUlmEP7S7yd1Y/edit?usp=sharing"

def download_file(url: str) -> bytes:
    """Download file and return bytes"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.RequestException:
        # Fallback to session-based download
        try:
            session = requests.Session()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = session.get(url, headers=headers, stream=True, allow_redirects=True)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Both download attempts failed for {url}: {e}")
            return None
            
    return response.content

def process_product_group(product_group, zip_file):
    """Process all URLs for a single product_id_colour"""
    local_alt_count = 0
    for record in product_group:
        url = record.get("URL")
        product_id_colour = record.get("ProductID_Colour")
        asset_type = record.get("Image Type")

        if url and url.startswith("http"):
            try:
                file_extension = os.path.splitext(url.split('?')[0])[-1] or '.jpg'
                
                if asset_type and asset_type.lower() == "primary" and product_id_colour:
                    filename = f"{product_id_colour}{file_extension}"
                elif asset_type and asset_type.lower() == "alt" and product_id_colour:
                    local_alt_count += 1
                    filename = f"{product_id_colour}_ALT-{local_alt_count}{file_extension}"
                else:
                    continue

                filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
                content = download_file(url)
                
                if content:
                    zip_file.writestr(filename, content)
                    print(f"Added to zip: {filename}")

            except Exception as e:
                print(f"Error processing {url}: {str(e)}")

@functions_framework.http
def process_sheet(request):
    """Cloud Function entry point"""
    try:
        # Initialize Google Sheets client
        credentials = service_account.Credentials.from_service_account_file(
            'secret/sheet-reader-key.json',
            scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        )
        client = gspread.authorize(credentials)
        
        # Get sheet data
        sheet = client.open_by_url(SHEET_URL).sheet1
        data = sheet.get_all_records()
        
        # Create zip in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Group and process records
            sorted_data = sorted(data, key=lambda x: x.get("ProductID_Colour"))
            product_groups = [(k, list(g)) for k, g in groupby(sorted_data, key=lambda x: x.get("ProductID_Colour")) if k]
            
            # Process groups in parallel
            with ThreadPoolExecutor(max_workers=16) as executor:
                futures = [executor.submit(process_product_group, group, zip_file) 
                          for _, group in product_groups]
                for future in futures:
                    future.result()  # Wait for all downloads to complete
        
        # Upload to GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        blob_name = f'downloads/image_pack_{timestamp}.zip'
        blob = bucket.blob(blob_name)
        
        blob.upload_from_string(
            zip_buffer.getvalue(),
            content_type='application/zip'
        )
        
        # Generate download URL (valid for 1 hour)
        url = blob.generate_signed_url(
            version="v4",
            expiration=3600,
            method="GET"
        )
        
        return {'download_url': url}
        
    except Exception as e:
        return {'error': str(e)}, 500