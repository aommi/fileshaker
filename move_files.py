# move_files.py

from datetime import datetime

def move_files(config, files_to_process, primary_name, today_date):
    primary_folder = config["source_folder_path"] / f"Primary_{today_date}"
    alt_folder = config["source_folder_path"] / f"ALT_{today_date}"
    primary_folder.mkdir(parents=True, exist_ok=True)
    alt_folder.mkdir(parents=True, exist_ok=True)

    is_primary_moved = False
    num_alts = 0
    alt_folder_name_logged = ""

    if files_to_process:
        first_file = files_to_process[0]
        file_extension = first_file.suffix
        new_primary_path = primary_folder / (primary_name + file_extension)
        first_file.rename(new_primary_path)
        is_primary_moved = True

        for index, file_path in enumerate(files_to_process[1:], start=1):
            file_extension = file_path.suffix
            alt_name = f"{primary_name}_ALT_{config['alphabet'][index-1]}{file_extension}"
            new_alt_file_path = alt_folder / alt_name
            file_path.rename(new_alt_file_path)
            num_alts += 1
            alt_folder_name_logged = str(alt_folder)

    return is_primary_moved, num_alts, primary_folder, alt_folder_name_logged