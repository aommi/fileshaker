# search-for-files.py

import os

def search_for_files(source_folder_path, vpn, alt_vpn):
    return [
        source_folder_path / filename
        for filename in os.listdir(source_folder_path)
        if (vpn in filename.lower() or alt_vpn in filename.lower()) and not (source_folder_path / filename).is_dir()
    ]