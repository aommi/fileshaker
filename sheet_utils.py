import os
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

class SheetUtils:
    def __init__(self):
        load_dotenv()
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        
        # Get base directory and create Path object
        base_dir = Path(os.getenv('BASE_DIR'))
        
        # Combine base_dir with relative credential paths
        reader_creds = os.getenv('READER_CREDENTIALS')
        writer_creds = os.getenv('WRITER_CREDENTIALS')
        
        self.reader_credentials_path = str(base_dir / reader_creds)
        self.writer_credentials_path = str(base_dir / writer_creds)
        
        # Verify paths exist
        if not Path(self.reader_credentials_path).exists():
            raise FileNotFoundError(f"Reader credentials not found at: {self.reader_credentials_path}")
        if not Path(self.writer_credentials_path).exists():
            raise FileNotFoundError(f"Writer credentials not found at: {self.writer_credentials_path}")
            
        # Initialize clients
        self.reader_client = self.authenticate(self.reader_credentials_path)
        self.writer_client = self.authenticate(self.writer_credentials_path)

    def authenticate(self, credentials_path):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, self.scope)
        return gspread.authorize(credentials)

    def read_sheet_data(self, client, sheet_key, sheet_gid, columns=None):
        """
        Read data from a Google Sheet
        Args:
            client: Authenticated gspread client
            sheet_key: The key of the spreadsheet
            sheet_gid: The ID of the worksheet
            columns: Optional list of column names to fetch (default: all columns)
        """
        sheet = client.open_by_key(sheet_key).get_worksheet_by_id(sheet_gid)
        
        if not columns:
            return sheet.get_all_records()
            
        # Get all records with specific columns
        all_records = sheet.get_all_records()
        return [{col: row[col] for col in columns if col in row} for row in all_records]

    def write_to_sheet(self, client, sheet_key, sheet_gid, row_data):
        sheet = client.open_by_key(sheet_key).get_worksheet_by_id(sheet_gid)
        sheet.append_row(row_data)