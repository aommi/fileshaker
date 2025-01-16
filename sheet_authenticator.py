# sheet-authenticator.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SheetAuthenticator:
    def __init__(self, credentials_path, scope):
        self.credentials_path = credentials_path
        self.scope = scope

    def authenticate(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, self.scope)
        return gspread.authorize(credentials)