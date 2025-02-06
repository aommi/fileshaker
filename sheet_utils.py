import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

class SheetUtils:
    def __init__(self):
        load_dotenv()
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.reader_credentials_path = os.getenv('READER_CREDENTIALS')
        self.writer_credentials_path = os.getenv('WRITER_CREDENTIALS')
        self.reader_client = self.authenticate(self.reader_credentials_path)
        self.writer_client = self.authenticate(self.writer_credentials_path)

    def authenticate(self, credentials_path):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, self.scope)
        return gspread.authorize(credentials)

    def read_sheet_data(self, client, sheet_key, sheet_gid):
        sheet = client.open_by_key(sheet_key).get_worksheet_by_id(sheet_gid)
        return sheet.get_all_records()

    def write_to_sheet(self, client, sheet_key, sheet_gid, row_data):
        sheet = client.open_by_key(sheet_key).get_worksheet_by_id(sheet_gid)
        sheet.append_row(row_data)