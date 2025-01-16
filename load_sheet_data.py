# load-sheet-data.py

def load_sheet_data(renamer_client, config):
    renamer_sheet = renamer_client.open_by_url(config["sheets"]["renamer"]["url"]).sheet1
    return renamer_sheet.get_all_records()